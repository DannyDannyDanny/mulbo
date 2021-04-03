FROM node:15
WORKDIR /usr/src/app
COPY nodeJS/package*.json ./

RUN npm install

COPY nodeJS/. .
EXPOSE 8081
CMD ["node", "server.js"]
