未完成

**test**

```shell script
py.test --count=100 -x --repeat-scope=session
py.test --repeat-scope=class
```
**test code coverage**
```shell script
py.test --cov=flask_blog test/
```
