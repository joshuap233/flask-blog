FROM tiangolo/meinheld-gunicorn:python3.7

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

RUN pip install flask

RUN mkdir -p /app

COPY ./app /app/app

COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ENV FLASK_ENV production
