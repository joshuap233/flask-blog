from app.model.db import User
from app.utils import generate_res
from .blueprint import api


@api.route('/user/about')
def about():
    return generate_res(data=User.query.first().user_about)

# @api.route('/user/about')
# def user_view():
#     return jsonify({
#         'status': 'success',
#         'data': {
#             "about": {"blocks":[{"key":"4jc4v","text":"关于本人","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"id":"关于本人"}},{"key":"cem1n","text":"it小学生","type":"unordered-list-item","depth":0,"inlineStyleRanges":[{"offset":0,"length":5,"style":"STRIKETHROUGH"}],"entityRanges":[],"data":{}},{"key":"2su85","text":"愤青,","type":"unordered-list-item","depth":0,"inlineStyleRanges":[{"offset":0,"length":2,"style":"STRIKETHROUGH"}],"entityRanges":[],"data":{}},{"key":"6mrkb","text":"没经历过社会的摩擦","type":"unordered-list-item","depth":0,"inlineStyleRanges":[{"offset":0,"length":9,"style":"STRIKETHROUGH"}],"entityRanges":[],"data":{}},{"key":"bss9f","text":"十万个为什么","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"uph","text":"热爱技术","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"449md","text":"大学本科在读","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"1j7hc","text":"富强民主文明和谐","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"dpgch","text":"自由平等公正法制","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"507m9","text":"爱国敬业诚信友善","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"d26r","text":"富強 民主 文明 和諧","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"6vjtc","text":"自繇 平等 公正 法治 ","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"as92h","text":"愛國 敬業 誠信 友善","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"aa6so","text":"Prosperity Democracy Civility Harmony","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"146ck","text":"Freedom Equality Justice RuleOfLaw ","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"1u1j7","text":"Patriotism Dedication Integrity Friendship","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"b8dlb","text":"부강 민주 문명 조화","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"6vve7","text":"자유 평등 공정, 법치","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"d889o","text":"애국 직업정신 성실과신용 우호","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"3obth","text":"正在拜读:","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"nodeAttributes":{}}},{"key":"50v57","text":"他改变了中国(手动狗头)","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":6,"key":0}],"data":{"nodeAttributes":{}}}],"entityMap":{"0":{"type":"LINK","mutability":"MUTABLE","data":{"href":"https://www.baidu.com/s?wd=%E4%BB%96%E6%94%B9%E5%8F%98%E4%BA%86%E4%B8%AD%E5%9B%BD&rsv_spt=1&rsv_iqid=0xdb5b2c6800019604&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_sug3=18&rsv_sug1=11&rsv_sug7=100","target":None,"nodeAttributes":{}}}}}
#         }})
