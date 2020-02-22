from flask import request

from app.model.db import Post
from app.utils import generate_res
from .blueprint import api


# @api.route('/post')
# def post_view():
#     post = Post.query.get_or_404(request.args.get('id'))
#     return generate_res(data={
#         'id': post.id,
#         'title': post.title,
#         'article': post.article
#     })


@api.route('/post')
def post_view():
    return generate_res(
        data={
            "id": 1,
            "title": "并发编程",
            "article": {"blocks":[{"key":"e3ouk","text":"import requests\nimport threading\ndef test2():\n    def request(url):\n        t = threading.Thread(target=lambda _: requests.get(_), args=(url,))\n        t.start()\n        return t\n    print('开始请求url:', URL1)\n    request(URL1)                         \n    print('开始请求url:', URL2)     # 非阻塞\n    request(URL2)\ntest2()\n","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"nodeAttributes":{},"syntax":"python"}},{"key":"duat5","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"2ugee","text":"import requests\nimport threading\ndef test2():\n    def request(url):\n        t = threading.Thread(target=lambda _: requests.get(_), args=(url,))\n        t.start()\n        return t\n    print('开始请求url:', URL1)\n    request(URL1)                         \n    print('开始请求url:', URL2)     # 非阻塞\n    request(URL2)\ntest2()","type":"code-block","depth":0,"inlineStyleRanges":[{"offset":0,"length":6,"style":"COLOR-8959A8"},{"offset":16,"length":6,"style":"COLOR-8959A8"},{"offset":33,"length":3,"style":"COLOR-8959A8"},{"offset":50,"length":3,"style":"COLOR-8959A8"},{"offset":104,"length":6,"style":"COLOR-8959A8"},{"offset":170,"length":6,"style":"COLOR-8959A8"},{"offset":33,"length":12,"style":"COLOR-4271AE"},{"offset":50,"length":17,"style":"COLOR-4271AE"},{"offset":37,"length":5,"style":"COLOR-3E999F"},{"offset":54,"length":7,"style":"COLOR-3E999F"},{"offset":42,"length":2,"style":"COLOR-F5871F"},{"offset":61,"length":5,"style":"COLOR-F5871F"},{"offset":189,"length":10,"style":"COLOR-718C00"},{"offset":260,"length":10,"style":"COLOR-718C00"},{"offset":282,"length":5,"style":"COLOR-8E908C"}],"entityRanges":[],"data":{"nodeAttributes":{}}},{"key":"5h05h","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"4cj8k","text":"🤣💚💚👏💝💓😅👍😊","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"1atnc","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"eupff","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"7g8qg","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"f6qpk","text":"tes","type":"table-cell","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"tableKey":"fpq5c","colIndex":0,"rowIndex":0,"colSpan":1,"rowSpan":1}},{"key":"bqnv","text":"test","type":"table-cell","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"tableKey":"fpq5c","colIndex":1,"rowIndex":0,"colSpan":1,"rowSpan":1}},{"key":"5766n","text":"teste","type":"table-cell","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"tableKey":"fpq5c","colIndex":2,"rowIndex":0,"colSpan":1,"rowSpan":1}},{"key":"6v19u","text":"teste","type":"table-cell","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"tableKey":"fpq5c","colIndex":0,"rowIndex":1,"colSpan":1,"rowSpan":1}},{"key":"aru41","text":"dsafdf","type":"table-cell","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"tableKey":"fpq5c","colIndex":1,"rowIndex":1,"colSpan":1,"rowSpan":1}},{"key":"ce40k","text":"teste","type":"table-cell","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"tableKey":"fpq5c","colIndex":2,"rowIndex":1,"colSpan":1,"rowSpan":1}},{"key":"ap7s5","text":"adsfsdf","type":"table-cell","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"tableKey":"fpq5c","colIndex":0,"rowIndex":2,"colSpan":1,"rowSpan":1}},{"key":"8j8l1","text":"tesate","type":"table-cell","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"tableKey":"fpq5c","colIndex":1,"rowIndex":2,"colSpan":1,"rowSpan":1}},{"key":"epkdv","text":"teat","type":"table-cell","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"tableKey":"fpq5c","colIndex":2,"rowIndex":2,"colSpan":1,"rowSpan":1}},{"key":"3cvv2","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}
        })
