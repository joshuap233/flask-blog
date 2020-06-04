FROM mysql:8.0.19

RUN echo "Asia/shanghai" > /etc/timezone;


COPY ./init.sql /docker-entrypoint-initdb.d/

