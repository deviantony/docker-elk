FROM node:8.2

ADD package.json        /app/package.json
ADD package-lock.json   /app/package-lock.json

WORKDIR /app
RUN npm install

ADD src/                /app/src
ADD tsconfig.json       /app/tsconfig.json

RUN npm run build

CMD ["npm", "start"]