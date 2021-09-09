FROM python:latest

RUN apt update && apt upgrade -y
RUN apt install python3-pip -y
RUN apt install ffmpeg -y

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm

RUN mkdir /VideoPlayerBot
COPY . /VideoPlayerBot
WORKDIR /VideoPlayerBot

RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

CMD python3 -m bot
