FROM tiangolo/meinheld-gunicorn:python3.7

COPY ./app /app/app

#COPY ./setup.py /app/setup.py

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ENV FLASK_ENV production
