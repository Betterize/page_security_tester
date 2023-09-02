/**
 * page-security-test controller
 */

import { factories } from "@strapi/strapi";
import { notify_tests_runner } from "../../../utils/queue";
import { notify_administrator } from "../../../utils/email";
import { log, HookState } from "../../../utils/logger";

const collection = "verification code controller";

// ------------------------------------------------------------------------
class UnprocessableEntityError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "UnprocessableEntityError";
  }
}

class NotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "NotFoundError";
  }
}

class ConflictError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "UnprocessableEntityError";
  }
}

// ------------------------------------------------------------------------

async function setup_status(id: number, status: string, message?: string) {
  let data: { [key: string]: unknown } = {
    status: status,
  };

  if (message) {
    data.error_msg = message;
  }

  try {
    const entry = await strapi.entityService.update(
      "api::page-security-test.page-security-test",
      id,
      {
        data: data,
      }
    );

    log(
      collection,
      HookState.none,
      `Marked collection as ${status} and updated error_msg`
    );
  } catch (err) {
    log(collection, HookState.none, `Unable to update entity. Error: ${err}`);
  }
}

async function process_data(id: number, website: string) {
  try {
    await setup_status(id, "waiting");
    await notify_tests_runner(JSON.stringify({ id: id, website: website }));

    log(
      collection,
      HookState.afterCreate,
      `Successfully added message to queue`
    );
  } catch (err) {
    await setup_status(
      id,
      "failed",
      `Unable to add message to queue. Error: ${err}`
    );

    try {
      await notify_administrator(`${err}`);

      log(
        collection,
        HookState.afterCreate,
        `Unable to add message to queue. Notified administrator. Error: ${err}`
      );
    } catch (err) {
      log(
        collection,
        HookState.afterCreate,
        `Error!. Unable to send email. ${err}`
      );
    }

    throw new Error(`Fatal error ocurred while data processing ${err}`);
  }
}

async function get_entry(id: number) {
  const entry = await strapi.entityService.findOne(
    "api::page-security-test.page-security-test",
    id
  );

  if (!entry) {
    throw new NotFoundError(`Can not found security scan with id: ${id}`);
  }

  if (entry.status != "unconfirmed") {
    throw new ConflictError(`Scan with ${id} already confirmed`);
  }

  return entry;
}

function validate_body(body: object) {
  if (!("code" in body)) {
    throw new UnprocessableEntityError(
      `No code field was given in body. Body: ${JSON.stringify(body)}`
    );
  }

  if (!("id" in body)) {
    throw new UnprocessableEntityError(
      `No id field was given in body. Body: ${JSON.stringify(body)}`
    );
  }

  if (typeof body.id != "number") {
    throw new UnprocessableEntityError(
      `Invalid type od id field. This field must be number. Body: ${JSON.stringify(
        body
      )}`
    );
  }

  if (typeof body.code != "string") {
    throw new UnprocessableEntityError(
      `Invalid type od code field. This field must be string. Body: ${JSON.stringify(
        body
      )}`
    );
  }
}

// ------------------------------------------------------------------------

export default factories.createCoreController(
  "api::page-security-test.page-security-test",
  ({ strapi }) => ({
    async verify_code(ctx) {
      const data = ctx.request.body;

      try {
        validate_body(data);
        const db_data = await get_entry(data.id);

        if (db_data.verification_code != data.code) {
          throw new ConflictError(
            `Given code: ${data.code} not match with code of scan with id: ${data.id}`
          );
        }

        await process_data(db_data.id, db_data.website);

        ctx.status = 200;
      } catch (err) {
        ctx.body = err.message;

        if (err instanceof UnprocessableEntityError) {
          ctx.status = 422;
        } else if (err instanceof ConflictError) {
          ctx.status = 409;
        } else {
          ctx.status = 500;
        }
      }
    },
  })
);
