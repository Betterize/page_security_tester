FROM node:16-bullseye-slim
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

WORKDIR /opt/app
COPY . .

RUN npm install

RUN npm run build

EXPOSE 1337
CMD ["npm", "run", "start"]