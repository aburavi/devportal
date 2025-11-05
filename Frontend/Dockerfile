# build stage
FROM node:12-alpine AS build-stage

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package*.json yarn.lock ./
RUN yarn install
RUN yarn add @vue/cli@latest -g

COPY . /app
RUN yarn run build

# production stage
FROM nginx:stable-alpine as final-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
#RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]