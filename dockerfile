FROM node:12

WORKDIR /app

RUN apt-get update || : && apt-get install python -y
RUN apt-get install ffmpeg -y

COPY package*.json ./

RUN npm install

COPY . .

CMD [ "node", "index.js" ]