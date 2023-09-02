FROM node:18-bullseye

WORKDIR /app
COPY . .

RUN npm install

ENV NODE_ENV=production

CMD ["npm", "run", "docker"]
