FROM python:3.6

WORKDIR /app

RUN apt-get -y update && apt-get install -y ffmpeg


COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt


COPY . .

CMD [ "python3", "./bot.py" ]
