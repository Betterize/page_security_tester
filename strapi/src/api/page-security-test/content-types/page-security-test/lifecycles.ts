import { log, HookState } from "../../../../utils/logger";
import { notify_tests_runner } from "../../../../utils/queue";
import {
  notify_administrator,
  sendEmail,
  EmailType,
  sendEmailWithAttachments,
} from "../../../../utils/email";
import { getReport, ScanReport } from "../../../../utils/scan_report";
import { errors } from "@strapi/utils";
const { ApplicationError } = errors;

const collection = "page-security-test";

async function setup_failed_status(id: number, message: string) {
  try {
    const entry = await strapi.entityService.update(
      "api::page-security-test.page-security-test",
      id,
      {
        data: {
          status: "failed",
          error_msg: message,
        },
      }
    );
    log(
      collection,
      HookState.afterCreate,
      `Marked collection as failed and updated error_msg`
    );
  } catch (err) {
    log(
      collection,
      HookState.afterCreate,
      `Unable to update entity. Error: ${err}`
    );
  }
}

export default {
  async beforeCreate(event) {
    const data = event.params.data;

    if (!data.accepted_regulations) {
      throw new ApplicationError(
        "Can not create security scan with not accepted scan regulations"
      );
    }
  },
  async afterCreate(event) {
    const { result } = event;
    log(
      collection,
      HookState.afterCreate,
      `Created page security test with id: ${result.id}`
    );

    try {
      await notify_tests_runner(
        JSON.stringify({ id: result.id, website: result.website })
      );
      log(
        collection,
        HookState.afterCreate,
        `Successfully added message to queue`
      );
    } catch (err) {
      await setup_failed_status(
        result.id,
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
    }
  },
  async afterCreateMany(event) {
    const { result } = event;
    log(collection, HookState.afterCreateMany, JSON.stringify(result));
  },
  async beforeUpdate(event) {
    const id = event.params.where.id;
    const data = event.params.data;

    if ("accepted_regulations" in data && !data.accepted_regulations) {
      throw new ApplicationError("Can not unaccepted scan regulations");
    }

    const entry = await strapi.entityService.findOne(
      "api::page-security-test.page-security-test",
      id
    );

    if (entry.status == "finished" || entry.status == "failed") {
      throw new ApplicationError(
        `Can not update ${entry.status} page security scan`
      );
    }

    log(collection, HookState.beforeUpdate, `Updated entry with id: ${id}`);
  },
  async afterUpdate(event) {
    const { result } = event;

    log(
      collection,
      HookState.afterUpdate,
      `Updated entry with id: ${result.id}`
    );

    if (result.status == "finished") {
      try {
        const content = await getReport(result as ScanReport);

        await sendEmailWithAttachments(
          {
            template_data: { website: result.website },
            to: result.email,
            from: process.env.EMAIL_FROM,
          },
          EmailType.ScanFinished,
          [
            {
              filename: "report.zip",
              content: content,
            },
          ]
        );
      } catch (e) {
        log(collection, HookState.afterUpdate, `Unable to send report: ${e}`);
      }
    }

    if (result.status == "failed") {
      await sendEmail(
        {
          template_data: " ",
          to: result.email,
          from: process.env.EMAIL_FROM,
        },
        EmailType.ScanFailed
      );
    }
  },
  async afterUpdateMany(event) {
    const { result } = event;
    log(collection, HookState.afterUpdateMany, JSON.stringify(result));
  },
  async afterDelete(event) {
    const { result } = event;
    log(collection, HookState.afterDelete, JSON.stringify(result));
  },
  async afterDeleteMany(event) {
    const { result } = event;
    log(collection, HookState.afterDeleteMany, JSON.stringify(result));
  },
};
