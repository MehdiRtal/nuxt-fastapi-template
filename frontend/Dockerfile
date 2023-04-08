FROM node:lts-alpine

WORKDIR /app

COPY package.json ./

RUN npm install --package-lock && npm cache clean --force

COPY ./ ./

RUN npm run build

RUN npm prune --production

EXPOSE 3000

CMD [ "node", ".output/server/index.mjs" ]