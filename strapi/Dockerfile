
FROM node:16-bullseye-slim
ARG NODE_ENV=development
ENV NODE_ENV=${NODE_ENV}

WORKDIR /opt/app
COPY . .

WORKDIR /opt/app/src/extensions/strapi-plugin-react-editorjs
RUN npm install

WORKDIR /opt/app
RUN npm install

RUN npm run build

EXPOSE 1337
CMD ["npm", "run", "develop"]