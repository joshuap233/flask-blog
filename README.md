TODO:
 my_config update
 add https 

## 开发: 
顶层目录创建.env文件
添加如下环境变量MAIL_PASSWORD,MAIL_USERNAME,API_SECURITY_STRING,SENTRY_DSN选填
- FLASK_APP=app.main:app
- FLASK_DEBUG=1
- FLASK_ENV=development
- MYSQL_ROOT_PASSWORD=root
- MYSQL_ADDRESS=127.0.0.1:3306 # 数据库ip:端口
- DB_NAME=pro_blog # 数据库名
- SERVER_NAME=127.0.0.1:5000 # 服务器域名:端口
- SECRET_KEY=   # 安全密钥,随机字符串,建议用os.urandom(32)生成
- JWT_SECRET_KEY= # 安全密钥,建议随机字符串,建议用os.urandom(32)生成
- \#MAIL_PASSWORD=  #邮件密码
- \#MAIL_USERNAME=  #邮件用户名
- \#API_SECURITY_STRING=  # 接口添加随机字符串
- \#SENTRY_DSN=  # sentry  错误处理集成


## 使用:
修改docker-compose配置
- MYSQL_ROOT_PASSWORD #必填 数据库密码 (两个改MYSQL_ROOT_PASSWORD都要,并且必须相同)
- SERVER_NAME: #必填 域名/ip
- SECRET_KEY #必填 flask密钥,请勿泄漏,建议用 python os.urandom(32)生成
- JWT_SECRET_KEY #必填 token密钥,请勿泄漏,建议用 python os.urandom(32)生成
- SENTRY_DSN #选填 sentry错误集成,参考参见:https://sentry.io/for/flask/
- MAIL_PASSWORD #选填 邮件服务器密码
- MAIL_USERNAME #选填 邮件服务器用户名
- API_SECURITY_STRING #必填,随机字符串,用于加密api

ssl 配置:
nginx/project.nginx.config
ssl_certificate /etc/nginx/certs/your_site_crt_file.crt;
ssl_certificate_key /etc/nginx/certs/your_site_crt_file.key;

nginx/project.nginx.config
修改 shushugo.com 为自己的域名

```bash
apt install docker-compose
bash run_docker.sh

- sqlalchemy 查询缓存
- nginx 接口缓存
- ngnix接口限浏览
