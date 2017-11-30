FROM node:carbon

WORKDIR /usr/src/app

COPY package.json yarn.lock ./

# install dependencies
RUN yarn

COPY ./ ./

RUN cd ./client && yarn

# build react app
RUN yarn build

EXPOSE 8080

CMD ["yarn", "start-prod"]