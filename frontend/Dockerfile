FROM node:alpine
WORKDIR /usr/src/app
RUN yarn global add http-server
COPY package.json yarn.lock ./
RUN yarn install && yarn cache clean
COPY . .
RUN yarn build
EXPOSE 8080
CMD [ "http-server", "dist" ]
