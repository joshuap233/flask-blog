#!/usr/bin/env bash
# flask 开始启动的时候连接数据总是断开,找了几天没找出原因,所以直接暴力死循环,直到构建成功为止
yarn build

while  [[ $? != 0 ]]
do
 sleep 20
 echo 'yarn build failed'
 yarn build
done

pm2-runtime yarn --interpreter bash --name api -- start
