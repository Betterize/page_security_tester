export default ({ env }) => ({
  email: {
    config: {
      provider: "strapi-provider-email-ovh",
      providerOptions: {
        user: env("EMAIL_ADDRESS"),
        pass: env("EMAIL_PASSWORD"),
      },
      settings: {
        defaultFrom: env("EMAIL_ADDRESS"),
        defaultReplyTo: env("EMAIL_ADDRESS"),
      },
    },
  },
});
