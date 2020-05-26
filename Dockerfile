FROM python:3.7.7-alpine3.11

RUN echo http://mirrors.aliyun.com/alpine/v3.11/main/ > /etc/apk/repositories

#RUN apk update && apk add libressl-dev libffi-dev build-base python3-dev mariadb-dev g++ make && rm -f /var/cache/apk/*
RUN apk update && apk add python3-dev mariadb-dev build-base  && rm -f /var/cache/apk/*

WORKDIR /app

COPY . .

# specify pip soucre to boost install (China:https://mirrors.aliyun.com/pypi/simple/)
RUN pip install -r requirements-pro.txt -i https://mirrors.aliyun.com/pypi/simple/

