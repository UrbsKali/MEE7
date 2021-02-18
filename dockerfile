FROM node:12

WORKDIR /app
RUN wget -q https://ftp-master.debian.org/keys/release-10.asc -O- | apt-key add -
RUN echo "deb http://deb.debian.org/debian buster non-free" >> /etc/apt/sources.list
RUN apt-get update || : && apt-get install python -y
RUN apt-get install ffmpeg -y
RUN apt-get install libttspico-utils -y

COPY package*.json ./

RUN npm install

COPY . .

CMD [ "node", "index.js" ]