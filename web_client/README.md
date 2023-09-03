## .env

List of variable with example values

```
PUBLIC_STRAPI_TOKEN="i am example value"
PUBLIC_STRAPI_BASE_URL="http://localhost:1337"
```

Please be aware that you should provide individual correct value of `PUBLIC_STRAPI_TOKEN`. To do this you need login to your strapi and generate API Token. Check [here](https://docs.strapi.io/user-docs/settings/API-tokens) if you don't know how to do it.

## No docker run

If you want to run this service locally without docker you need to have node installed. Then just install all dependencies with `npm install` and run with in development mode with:

```
npm run dev
```

To build and run use bellow commands:

```
npm run build
npm run preview
```
