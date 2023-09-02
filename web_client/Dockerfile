FROM node:18-bullseye

WORKDIR /app
COPY . .

RUN npm install
RUN npm run build

ENV NODE_ENV=production

CMD ["npm", "run", "preview_all_hosts"]
