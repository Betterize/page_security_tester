"use strict";

const {
  winston,
  formats: { prettyPrint, levelFilter },
} = require("@strapi/logger");

import DailyRotateFile from "winston-daily-rotate-file";

export default {
  level: "http",
  transports: [
    new winston.transports.Console({
      level: "http",
      format: winston.format.combine(
        levelFilter("http"),
        prettyPrint({ timestamps: "YYYY-MM-DD hh:mm:ss.SSS" })
      ),
    }),
    new DailyRotateFile({
      level: "http",
      filename: "logs/strapi/strapi-%DATE%.log",
      datePattern: "YYYY-MM-DD",
      format: winston.format.combine(
        levelFilter("http"),
        winston.format.timestamp(),
        winston.format.json()
      ),
    }),
  ],
};
