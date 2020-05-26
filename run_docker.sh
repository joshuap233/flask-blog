#!/usr/bin/env bash

echo killing old docker processes
# --env-file /dev/null 防止自动读取当前目录.env文件
docker-compose --env-file /dev/null rm -fs

echo building docker containers
#docker-compose build --no-cache
docker-compose --env-file /dev/null up --build -d --force-recreate
