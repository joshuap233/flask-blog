未完成

**test**

```shell script
py.test --count=100 -x --repeat-scope=session -s
```
**test code coverage**
```shell script
py.test --cov=flask_blog test/ --repeat-scope=session -s
```
## TODO
错误处理
邮箱登录
密码找回
文章分页(归档)

## admin api
- [注册](#register)
- [登录](#login)
- [登出](#logout)
- [获取图片](#images)
- [修改单篇文章](#post)
- [请求所有文章](#post)




### register
url
```
/api/admin/auth/register/
```

**请求方法**:
POST

**请求参数**

| 名称| 类型| 说明| 是否必须|
| --- | --- | --- | --- |
|phone_number| string| | [] |
|email| string| | [] |
|nickname| string| | [x] |
|username| string| 用于登录 |[x] |
|password| string| | [x]|
|user_about| string|  | [] |


**返回参数**

| 名称| 类型| 说明|
| --- | --- | --- |
|status| success/failed| | 
|msg| | | 


### login
url:
```
/api/admin/auth/login/
```
**请求方法**:
POST

**请求参数**

| 名称| 类型| 说明| 
| --- | --- | --- |
|password| string| | 
|username| string| | 

**返回参数**


### logout

url:
```
/api/admin/auth/logout/
```
**请求方法**:
DELETE

**请求头**

| 名称| 类型| 说明| 
| --- | --- | --- |
|identify| string| 用户id| 
|token| string| | 


### images

```
/api/admin/posts/images/
```
**请求方法**:
GET, PUT

**简要描述**
get请求图片
put上传图片

**GET, PUT请求头**

| 名称| 类型| 说明| 
| --- | --- | --- |
|identify| string| 用户id| 
|token| string| | 


**GET请求参数**

| 名称| 类型| 说明| 
| --- | --- | --- |
|id| string| 文章id| 
|filename| string|图片名| 


**PUT请求参数**

| 名称| 类型| 说明| 
| --- | --- | --- |
|images| form|上传的图片| 
|id| int| 文章id| 


### post
url

```
/api/admin/posts/
```

**请求方法**
GET, PUT, POST

**简要描述**
get 获取单篇文章内容
put 修改文章
post 新建文章

**GET,PUT,POST请求头**

| 名称| 类型| 说明| 
| --- | --- | --- |
|identify| string| 用户id| 
|token| string| | 


**GET请求参数**

| 名称| 类型| 说明| 
| --- | --- | --- |
|id| int| 文章id|

**GET返回参数**

| 名称| 类型| 说明| 
| --- | --- | --- |
|id| int| 文章id|
|contents| string| 文章内容|
|title| string| 文章标题|


 **POST请求参数**
 
| 名称| 类型| 说明| 
| --- | --- | --- |
|create_date| int| 文章创建的时间戳|

**POST返回参数**

| 名称| 类型| 说明| 
| --- | --- | --- |
|id| int| 文章id|

 **PUT请求参数**
 
| 名称| 类型| 说明| 是否必须|
| --- | --- | --- | --- |
|id| int| 文章id| [x] |
|tags| list|标签列表,没有标签则为空|[x] |
|contents| string|文章内容(markdown)|[] |
|title| string|文章标题|[x] |
|publish| boolean|是否发布|[] |
|change_date| int|文章修改日期|[x]|


### posts

url

```
/api/admin/posts/all/
```

**请求方法**
GET

**简要描述**
请求所有文章

**G请求头**

| 名称| 类型| 说明| 
| --- | --- | --- |
|identify| string| 用户id| 
|token| string| | 


**返回参数**
 
| 名称| 类型| 说明|
| --- | --- | --- |
|id| int| 文章id| [x] |
|tags| list|标签列表,没有标签则为空|
|title| string|文章标题|
|publish| boolean|是否发布|
|change_date| int|文章创建日期|
|change_date| int|文章修改日期|
