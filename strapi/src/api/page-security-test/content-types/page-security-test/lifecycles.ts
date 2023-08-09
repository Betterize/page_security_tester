import { log, HookState } from "../../../../utils/logger";
import { notify_tests_runner } from "../../../../utils/queue";

const collection = "page-security-test";

export default {
  async afterCreate(event) {
    const { result } = event;
    log(
      collection,
      HookState.afterCreate,
      `Created page security test with id: ${result.id}`
    );

    try {
      await notify_tests_runner(result.website);
      log(
        collection,
        HookState.afterCreate,
        `Successfully added message to queue`
      );
    } catch (err) {
      log(
        collection,
        HookState.afterCreate,
        `Unable to add message to queue. Error: ${err}`
      );
    }
  },
  async afterCreateMany(event) {
    const { result } = event;
    log(collection, HookState.afterCreateMany, JSON.stringify(result));
  },
  async afterUpdate(event) {
    const { result } = event;
    log(
      collection,
      HookState.afterUpdate,
      `Updated entry with id: ${result.id}`
    );
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
