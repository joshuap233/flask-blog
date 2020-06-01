FROM nginx:1.17.10-alpine

RUN rm /etc/nginx/nginx.conf

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx/project.nginx.conf /etc/nginx/conf.d/

COPY ./nginx/nginx.conf /etc/nginx/

COPY ./app/app_admin/static/ /static/admin/

COPY ./app/app_frontend/static/ /static/fontend/

RUN mkdir -p /data && cd /data && mkdir -p cache
