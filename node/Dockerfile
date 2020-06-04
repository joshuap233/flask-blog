FROM node:13.14.0-buster-slim

RUN echo "Asia/shanghai" > /etc/timezone;


RUN  echo "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib\
\ndeb-src http://mirrors.aliyun.com/debian/ buster main non-free contrib\
\ndeb http://mirrors.aliyun.com/debian-security buster/updates main\
\ndeb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\
\ndeb-src http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\
\ndeb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib\
\ndeb-src http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib" > /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
	apt-transport-https \
	ca-certificates \
	curl \
	gnupg \
	--no-install-recommends \
	&& curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
	&& echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
	&& apt-get update && apt-get install -y \
	google-chrome-stable \
	fontconfig \
	fonts-ipafont-gothic \
	fonts-wqy-zenhei \
	fonts-thai-tlwg \
	fonts-kacst \
	fonts-symbola \
	fonts-noto \
	fonts-freefont-ttf \
	--no-install-recommends \
	&& apt-get purge --auto-remove -y curl gnupg \
	&& rm -rf /var/lib/apt/lists/*

# Add Chrome as a user
RUN groupadd -r chrome && useradd -r -g chrome -G audio,video chrome \
	&& mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

# Run Chrome non-privileged
USER chrome

WORKDIR /home/chrome

COPY ./ /home/chrome

RUN cd /home/chrome/ && npm install --registry https://registry.npm.taobao.org/

EXPOSE 8888

CMD google-chrome --disable-gpu --headless & node ssr.js

# Autorun chrome headless with no GPU
#ENTRYPOINT [ "google-chrome" ]
#CMD [ "--headless", "--disable-gpu", "--remote-debugging-address=0.0.0.0", "--remote-debugging-port=9222" ]
