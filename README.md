使用
修改docker-compose配置
- MYSQL_ROOT_PASSWORD //必填 数据库密码 (两个改MYSQL_ROOT_PASSWORD都要,并且必须相同)
- SERVER_NAME: //必填 域名/ip
- SECRET_KEY //必填 flask密钥,请勿泄漏,建议用 python os.urandom(32)生成
- JWT_SECRET_KEY //必填 token密钥,请勿泄漏,建议用 python os.urandom(32)生成
- SENTRY_DSN //选填 sentry错误集成,参考参见:https://sentry.io/for/flask/
- MAIL_PASSWORD //选填 邮件服务器密码
- MAIL_USERNAME //选填 邮件服务器用户名
- API_SECURITY_STRING //必填,随机字符串,用于加密api


```bash
bash run_docker.sh
```


TODO:
- 缓存常用数据
