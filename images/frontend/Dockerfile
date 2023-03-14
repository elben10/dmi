FROM node:16 as dev

WORKDIR /app

COPY package.json yarn.lock ./
COPY packages/frontend/package.json ./packages/frontend/

RUN yarn workspace frontend install

COPY packages/frontend ./packages/frontend

CMD ["yarn", "workspace", "frontend", "dev"]

FROM dev as build

WORKDIR /app

RUN yarn workspace frontend build

FROM nginx:1.21.1-alpine as prod

COPY --from=build /app/packages/frontend/dist /usr/share/nginx/html
