// https://www.npmjs.com/package/winston
// https://www.npmjs.com/package/winston-daily-rotate-file

import { winston, formats } from "@strapi/logger";
import moment from "moment";
import DailyRotateFile from "winston-daily-rotate-file";

// this will be printed to fille with daily rotation
const transport_rotate = new DailyRotateFile({
  level: "http",
  filename: "logs/custom/strapi-%DATE%.log",
  datePattern: "YYYY-MM-DD",
});

const myFormat = winston.format.printf(
  ({ level, message, hook_state, collection, time, date }) => {
    return `[${date} ${time}] \u001b[32m${level}\u001b[39m: [${collection}] [${hook_state}] ${message}`;
  }
);

// this will be printed on console
const transport_console = new winston.transports.Console({
  level: "http",
  format: winston.format.combine(formats.levelFilter("http"), myFormat),
});

export const logger = winston.createLogger({
  transports: [transport_console, transport_rotate],
});

// --------------------------------------------------------------------------

export enum HookState {
  beforeCreate = "beforeCreate",
  beforeCreateMany = "beforeCreateMany",
  afterCreate = "afterCreate",
  afterCreateMany = "afterCreateMany",
  beforeUpdate = "beforeUpdate",
  beforeUpdateMany = "beforeUpdateMany",
  afterUpdate = "afterUpdate",
  afterUpdateMany = "afterUpdateMany",
  beforeDelete = "beforeDelete",
  beforeDeleteMany = "beforeDeleteMany",
  afterDelete = "afterDelete",
  afterDeleteMany = "afterDeleteMany",
  beforeCount = "beforeCount",
  afterCount = "afterCount",
  beforeFindOne = "beforeFindOne",
  afterFindOne = "afterFindOne",
  beforeFindMany = "beforeFindMany",
  afterFindMany = "afterFindMany",
  none = "none",
}

export function log(
  collection_type: string,
  hook_state: HookState,
  message: string
) {
  const time_stamp = moment();
  const date = time_stamp.format("YYYY-MM-DD");
  const time = time_stamp.format("HH:mm:ss.SSS");

  logger.log({
    level: "http", // it is required by strapi to pass log further
    date: date,
    time: time,
    hook_state: hook_state,
    collection: collection_type,
    message: message,
  });
}
