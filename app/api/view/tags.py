from flask import jsonify

from .blueprint import api


@api.route('/tags')
def tag_view():
    return jsonify({
        'status': 'success',
        'data': [
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
            }
        ]})


# @api.route('/tags/')
# def tags():
#     tags_ = Tag.query.all()
#     data = []
#     for tag in tags_:
#         data.append({
#             "name": tag.name,
#             "article": [{"id": post.id, "title": post.title} for post in tag.posts]
#         })
#     return generate_res('success', data=data)


"""   
  data:[
      {
            "name": "ubuntu",
            "article": [
                {
                    "id": 1,
                    "title": "title1"
                },
                {
                    "id": 2,
                    "title": "title2"
                },
                {
                    "id": 3,
                    "title": "title3"
                }
            ]
        },
        {
            "name": "linux",
            "article": [
                {
                    "id": 4,
                    "title": "title4"
                },
                {
                    "id": 5,
                    "title": "title5"
                },
                {
                    "id": 6,
                    "title": "title6"
                }
            ]
        }
    ])
"""
