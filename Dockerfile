# Debian Based Docker
FROM debian:latest

# Installing Packages
RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y

# Installing Pip Packages
RUN pip3 install -U pip

# Installing NodeJS
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt install -y nodejs && \
    npm i -g npm

# Copying Requirements
COPY requirements.txt /requirements.txt

# Installing Requirements
RUN cd /
RUN pip3 install -U -r requirements.txt
RUN mkdir /VideoPlayerBot
WORKDIR /VideoPlayerBot
COPY start.sh /start.sh

# Running Video Player Bot
CMD ["/bin/bash", "/start.sh"]
