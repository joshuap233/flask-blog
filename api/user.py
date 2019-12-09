from .blueprint import api
from flask import jsonify


@api.route('/user/about/')
def about():
    return jsonify({
        "data": "## 关于本人\n+ ~~IT小学生~~\n- ~~愤青~~,\n+ ~~没经历过社会的摩擦~~\n- 十万个为什么\n+ 热爱技术\n- 大学本科在读\n+ 富强民主文明和谐\n- 自由平等公正法制\n+ 爱国敬业诚信友善\n- 富強 民主 文明 和諧\n+ 自繇 平等 公正 法治 \n- 愛國 敬業 誠信 友善\n+ Prosperity Democracy Civility Harmony\n- Freedom Equality Justice RuleOfLaw \n+ Patriotism Dedication Integrity Friendship\n- 부강 민주 문명 조화\n+ 자유 평등 공정, 법치\n-  애국 직업정신 성실과신용 우호\n\n正在拜读:\n[他改变了中国](https://www.baidu.com/s?wd=%E4%BB%96%E6%94%B9%E5%8F%98%E4%BA%86%E4%B8%AD%E5%9B%BD&rsv_spt=1&rsv_iqid=0xdb5b2c6800019604&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_sug3=18&rsv_sug1=11&rsv_sug7=100)\n(手动狗头)\n"
    })
