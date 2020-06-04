FROM python:3.7.7-alpine3.11

RUN echo "Asia/shanghai" > /etc/timezone;


RUN echo http://mirrors.aliyun.com/alpine/v3.11/main/ > /etc/apk/repositories

#RUN apk update && apk add libressl-dev libffi-dev build-base python3-dev mariadb-dev g++ make && rm -f /var/cache/apk/*
RUN apk --no-cache update && apk --no-cache add python3-dev mariadb-dev build-base

WORKDIR /app

COPY ./app ./app

COPY ./gunicorn.conf.py .

COPY ./requirements-pro.txt ./requirements.txt

# specify pip soucre to boost install (China:https://mirrors.aliyun.com/pypi/simple/)
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
