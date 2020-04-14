# from flask import jsonify
#
# from app.model.db import Post
# from app.model.view_model import QueryView
# from app.utils import generate_res, format_time
# from .blueprint import api
#
#
# # @api.route('/archive')
# # def archive():
# #     query = QueryView()
# #     # TODO :按时间排序
# #     pagination = Post.search(**query.search_parameter)
# #     data = []
# #     for post in pagination.items:
# #         year, month, date = format_time(post.create_date, format_='%Y/%m/%d ').split('/')
# #         article = {"id": post.id, "title": post.title, "date": date}
# #         if len(data) == 0:
# #             data.append({"date": f'{year}-{month}', "articles": [article]})
# #             continue
# #         for item in data:
# #             if item.get('date') == f'{year}-{month}':
# #                 item["articles"].append(article)
# #             else:
# #                 data.append({"date": f'{year}-{month}', "articles": [article]})
# #     return generate_res(data=data)
#
#
# @api.route('/archive')
# def archive_view():
#     return jsonify({
#         'status': 'success',
#         'data': [
#             {
#                 "date": "2019-1",
#                 "articles": [
#                     {
#                         "id": 1,
#                         "title": "并发编程",
#                         "date": "1"
#                     },
#                     {
#                         "id": 2,
#                         "title": "搜索引擎查询",
#                         "date": "2"
#                     },
#                     {
#                         "id": 4,
#                         "title": "dns字典爆破",
#                         "date": "3"
#                     }
#                 ]
#             },
#             {
#                 "date": "2019-2",
#                 "articles": [
#                     {
#                         "id": 5,
#                         "title": "sql学习笔记(day1)",
#                         "date": "1"
#                     },
#                     {
#                         "id": 6,
#                         "title": "记录一些python小窍门",
#                         "date": "1"
#                     },
#                     {
#                         "id": 7,
#                         "title": "绕过验证码爬取学校cms",
#                         "date": "1"
#                     }
#                 ]
#             }
#         ]})
#
