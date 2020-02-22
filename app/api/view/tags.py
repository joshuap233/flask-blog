from app.utils import generate_res
from .blueprint import api


# @api.route('/tags')
# def tags():
#     return generate_res(data=[{
#         "id": tag.id,
#         "name": tag.name,
#         "count": tag.count
#     } for tag in Tag.query.all()])
#

@api.route('/tags')
def tag_view():
    return generate_res(
        data=[
            {
                "id": 1,
                "name": "ubuntu",
                "count": 5,
            },
            {
                "id": 2,
                "name": "linux",
                "count": 10
            },
            {
                "id": 3,
                "name": "python",
                "count": 3
            }, {
                "id": 4,
                "name": "java",
                "count": 3
            }, {
                "id": 5,
                "name": "javaScript",
                "count": 3
            }, {
                "id": 6,
                "name": "学习记录",
                "count": 3
            }, {
                "id": 7,
                "name": "docker",
                "count": 3
            }, {
                "id": 8,
                "name": "chrome",
                "count": 3
            },
        ])
