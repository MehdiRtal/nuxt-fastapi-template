FROM node:lts-alpine

WORKDIR /app

COPY ./package.json ./ ./package-lock.json ./

RUN npm ci

COPY ./ ./

RUN npx nuxi build

RUN npm prune --production
