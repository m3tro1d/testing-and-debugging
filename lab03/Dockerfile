FROM node:16.17.1

COPY package.json yarn.lock /app/

WORKDIR /app

RUN yarn install --pure-lockfile

COPY . /app

CMD ["yarn", "test"]
