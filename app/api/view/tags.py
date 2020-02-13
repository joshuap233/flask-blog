from app.model.db import Tag
from app.utils import generate_res
from .blueprint import api


@api.route('/tags')
def tags():
    return generate_res(data=[{
        "id": tag.id,
        "name": tag.name,
        "count": tag.count
    } for tag in Tag.query.all()])

#
# @api.route('/tags')
# def tag_view():
#     return jsonify({
#         'status': 'success',
#         'data': [
#             {
#                 "id": 1,
#                 "name": "ubuntu",
#                 "count": 5,
#             },
#             {
#                 "id": 2,
#                 "name": "linux",
#                 "count": 10
#             },
#             {
#                 "id": 3,
#                 "name": "python",
#                 "count": 3
#             }
#         ]})
