from .blueprint import api
from ..database import Tag
from ..utils import generate_res


@api.route('/tags/')
def tags():
    tags_ = Tag.query.all()
    data = []
    for tag in tags_:
        data.append({
            "name": tag.name,
            "article": [{"id": post.id, "title": post.title} for post in tag.posts]
        })
    return generate_res('success', 'tags', data=data)


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
