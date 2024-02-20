FROM node:lts-alpine

WORKDIR /app

COPY package.json ./

RUN npm install --package-lock && npm cache clean --force

COPY ./ ./

RUN npx nuxi build

RUN npm prune --production
