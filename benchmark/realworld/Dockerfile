# Stage 1: Build the Angular App
FROM node:18-alpine as build

WORKDIR /app

RUN addgroup -S mygroup && adduser -S myuser -G mygroup

COPY package*.json ./
RUN npm install

COPY . .

ENV PORT=4200

EXPOSE 4200

CMD [ "npm", "start" ]
