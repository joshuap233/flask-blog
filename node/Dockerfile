FROM node:14.3.0-alpine3.11

RUN echo http://mirrors.aliyun.com/alpine/v3.11/main/  > /etc/apk/repositories
RUN echo http://mirrors.aliyun.com/alpine/v3.11/community/  >> /etc/apk/repositories

RUN apk update && apk add --no-cache chromium nss freetype freetype-dev harfbuzz ca-certificates ttf-freefont nodejs

RUN npm set registry https://registry.npm.taobao.org/

# Tell Puppeteer to skip installing Chrome. We'll be using the installed package.
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

RUN npm install puppeteer


RUN addgroup -S pptruser && adduser -S -g pptruser pptruser \
    && mkdir -p /home/pptruser/Downloads /app \
    && chown -R pptruser:pptruser /home/pptruser \
    && chown -R pptruser:pptruser /app


USER pptruser


RUN mkdir -p app

RUN npm set registry https://registry.npm.taobao.org/

WORKDIR /app

COPY ./ /app/

RUN cd /app && npm install



EXPOSE 8888

CMD node ssr.js
