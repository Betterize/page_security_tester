"use strict";

/**
 * Module dependencies
 */
const nodemailer = require("nodemailer");
const { removeUndefined } = require("@strapi/utils");

module.exports = {
  init: (providerOptions = {}, settings = {}) => {
    return {
      send: async (options) => {
        const transporter = nodemailer.createTransport({
          host: "pro3.mail.ovh.net",
          port: 587,
          secure: false,
          auth: {
            user: providerOptions.user,
            pass: providerOptions.pass,
          },
          tls: {
            rejectUnauthorized: true,
            minVersion: "TLSv1.2",
          },
        });

        options.from = options.from || settings.defaultFrom;
        options.replyTo = options.replyTo || settings.defaultReplyTo;
        options.text = options.text || options.html;

        let msg = {
          from: options.from,
          to: options.to,
          cc: options.cc,
          bcc: options.bcc,
          replyTo: options.replyTo,
          subject: options.subject,
          html: options.text,
        };

        var info = await transporter.sendMail(removeUndefined(msg));
        return info;
      },
    };
  },
};
