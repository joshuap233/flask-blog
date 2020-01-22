未完成

**test**

```shell script
py.test --count=100 -x --repeat-scope=session -s
py.test  --repeat-scope=session -s
```
**test code coverage**
```shell script
py.test --cov=flask_blog test/ --repeat-scope=session -s
```
## TODO
错误处理
修改密码
手机号密码找回

## admin api
- [注册](#register)
- [登录](#login)
- [登出](#logout)
- [获取图片](#Images)
- [修改单篇文章](#post)
- [分页请求文章](#posts)




### register
- URL: ```/api/admin/auth/register/```
- Method: POST

*请求参数*

| 名称| 类型| 说明| 是否必须|
| --- | --- | --- | --- |
|phone_number| string| |  |
|email| string| | 是 |
|nickname| string| | 是 |
|username| string| 用于登录 |是 |
|password| string| | 是|
|user_about| string|  |  |


*返回参数*

| 名称| 类型| 说明|
| --- | --- | --- |
|status| success/failed| | 
|msg| | | 


### login
+ URL: ```/api/admin/auth/login/```
+ Method: POST

*请求参数*

| 名称| 类型| 说明| 
| --- | --- | --- |
|password| string| | 
|username| string| | 

*返回参数*
| 名称| 类型| 说明| 
| --- | --- | --- |
|id| string| 用户id| 
|token| string| 过期时间:3600s| 

### logout

+ URL: ```/api/admin/auth/logout/```
+ Method: DELETE
+ HTTP Headers: 
```
{
    "identify": "uid",
    "token": "token"
}
```

### Images
+ URL: ```/api/admin/images/```
+ Method: GET, PUT
+ Describe: get请求图片,put上传图片
+ HTTP Headers: 
```
{
    "identify": "uid",
    "token": "token"
}
```

*GET请求参数*

| 名称| 类型| 说明| 
| --- | --- | --- |
|id| string| 文章id| 
|filename| string|图片名| 


*PUT请求参数*

| 名称| 类型| 说明| 
| --- | --- | --- |
|images| form|上传的图片| 
|id| int| 文章id| 


### post
+ URL: ```/api/admin/posts/<int:pid>```
+ Method: GET, PUT, POST, DELETE
+ Describe: get获取单篇文章内容 put修改文章 post新建文章
+ HTTP Headers: 
```
{
    "identify": "uid",
    "token": "token"
}
```

*GET,PUT,DELETE路径参数*

| 名称| 类型| 说明| 
| --- | --- | --- |
|pid| int| 文章id|

*GET返回参数*

| 名称| 类型| 说明| 
| --- | --- | --- |
|id| int| 文章id|
|contents| string| 文章内容|
|title| string| 文章标题|


*POST请求参数*
 
| 名称| 类型| 说明| 
| --- | --- | --- |
|create_date| int| 文章创建的时间戳|

*POST返回参数*

| 名称| 类型| 说明| 
| --- | --- | --- |
|id| int| 文章id|

*PUT请求参数*
 
| 名称| 类型| 说明| 是否必须|
| --- | --- | --- | --- |
|tags| list|标签列表,没有标签则为空|是|
|contents| string|文章内容(markdown)| |
|title| string|文章标题|是 |
|publish| boolean|是否发布| |
|change_date| int|文章修改日期|是|


### posts
+ URL: ```/api/admin/posts/page/<int:page>```
+ Method: GET
+ Describe: 请求所有文章
+ HTTP Headers: 
```
{
    "identify": "uid",
    "token": "token"
}
```

*返回参数*
 
| 名称| 类型| 说明|
| --- | --- | --- |
|id| int| 文章id|  |
|tags| list|标签列表,没有标签则为空|
|title| string|文章标题|
|publish| boolean|是否发布|
|change_date| int|文章创建日期|
|change_date| int|文章修改日期|
