import fs from "fs";
import handlebars from "handlebars";
import nodemailer from "nodemailer";
import { HookState, log } from "./logger";

// -----------------------------------------------------------

export enum EmailType {
  NotifyAdministrator = "notify_administrator",
  TestFinished = "test_finished",
  ScanFailed = "scan_failed",
  ScanFinished = "scan_finished",
  VerifyCode = "verify_code",
}

interface NotifyAdmin {
  service: string;
  message: string;
}

export interface Email {
  to: string;
  from: string;
  template_data: NotifyAdmin | undefined | Object;
}

// -----------------------------------------------------------

function load_templates() {
  const enum_values = Object.values(EmailType) as string[];
  let result = {};

  for (let key of enum_values) {
    let data = fs.readFileSync(
      `./src/utils/email_templates/${key}.html`,
      "utf-8"
    );
    let [subject, body] = data.split("(*_*)");

    result[key] = { subject: subject, body: handlebars.compile(body) };
  }

  return result;
}

var templates = load_templates();

// -----------------------------------------------------------

export async function sendEmail(data: Email, type: EmailType) {
  await strapi.plugins["email"].services.email.send({
    to: data.to,
    from: data.from,
    subject: templates[type].subject,
    html: templates[type].body(data.template_data),
  });
}

// -----------------------------------------------------------

const transporter = nodemailer.createTransport({
  host: "pro3.mail.ovh.net",
  port: 587,
  secure: false,
  auth: {
    user: process.env.EMAIL_FROM,
    pass: process.env.EMAIL_PASSWORD,
  },
});

export async function sendEmailWithAttachments(
  data: Email,
  type: EmailType,
  attachments: Object[]
) {
  const mailOptions = {
    from: data.from,
    to: data.to,
    subject: templates[type].subject,
    html: templates[type].body(data.template_data),
    attachments: attachments,
  };

  transporter.sendMail(mailOptions, (error, _) => {
    if (error) {
      log("email with attachments", HookState.none, error);
    }
  });
}

// -----------------------------------------------------------

export async function notify_administrator(message: string) {
  await sendEmail(
    {
      to: process.env.EMAIL_ADMINISTRATOR,
      from: process.env.EMAIL_FROM,
      template_data: {
        message: message,
        service: "queue",
      },
    },
    EmailType.NotifyAdministrator
  );
}

export async function notify_about_test_finish() {
  await sendEmail(
    {
      to: process.env.EMAIL_ADMINISTRATOR,
      from: process.env.EMAIL_FROM,
      template_data: undefined,
    },
    EmailType.TestFinished
  );
}
