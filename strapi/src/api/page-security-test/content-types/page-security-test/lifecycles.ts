import { log, HookState } from "../../../../utils/logger";
import { notify_tests_runner } from "../../../../utils/queue";
import {
  notify_administrator,
  notify_about_test_finish,
} from "../../../../utils/email";

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
    const status = event.params.data.status;

    if (status == "finished" || status == "failed") {
      event.params.data.is_public = true;
    }

    log(
      collection,
      HookState.beforeUpdate,
      `Updated entry with id: ${event.params.data.id}`
    );
  },
  async afterUpdate(event) {
    const { result } = event;

    log(
      collection,
      HookState.afterUpdate,
      `Updated entry with id: ${result.id}`
    );

    if (result.status == "finished") {
      await notify_about_test_finish();
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
