FROM debian:buster

# install packages
RUN apt update &&\
    apt install -y\
        python3.7 python3-pip\
        libsdl2-2.0-0 libsdl2-dev\
        libsdl2-image-2.0-0 libsdl2-image-dev\
        libsdl2-mixer-2.0-0 libsdl2-mixer-dev\
        libsdl2-gfx-1.0-0 libsdl2-ttf-2.0-0

# add source
COPY . /app/
WORKDIR /app

# install python dep
RUN pip3 install discord pyboy pillow

# store /data
VOLUME [ "/data" ]

# on server start
CMD python3.7 src/bot.py
