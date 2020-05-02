FROM nginx:1.15.8-alpine

RUN rm /etc/nginx/nginx.conf

COPY ./nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf

COPY project.nginx.conf /etc/nginx/conf.d/
