FROM node:13.14.0-buster-slim

RUN echo "Asia/shanghai" > /etc/timezone;

RUN  echo "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib\
\ndeb-src http://mirrors.aliyun.com/debian/ buster main non-free contrib\
\ndeb http://mirrors.aliyun.com/debian-security buster/updates main\
\ndeb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\
\ndeb-src http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\
\ndeb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib\
\ndeb-src http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib" > /etc/apt/sources.list

RUN apt update && apt-get install -y yarn \
	&& apt autoremove -y && apt autoclean -y \
	&& rm -rf /var/lib/apt/lists/*

COPY ./ /home/

WORKDIR /home/app

COPY ./start.sh .

RUN cd /home/app && yarn --registry https://registry.npm.taobao.org/

 RUN yarn global add  pm2  --registry https://registry.npm.taobao.org/

CMD bash ./start.sh

