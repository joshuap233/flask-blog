from time import strftime, localtime

from .blueprint import api
from ..database import Post
from ..utils import generate_res


@api.route('/archive/<page>')
def archive(page):
    # per_page 写入config
    pagination = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=20, error_out=False)
    posts = pagination.items
    data = []
    for post in posts:
        timestamp = posts.date / 1000
        year, month, date = strftime('%Y-%m-%d', localtime(timestamp)).split("-")
        for item in data:
            articles = {"articles": post.id, "title": post.title, "date": date}
            if item['date'] == f'{year}-{month}':
                item["articles"].append(articles)
            else:
                data.append({"date": f'{year}-{month}', "articles": [articles]})
    return generate_res("success", "archive", data=data)


"""
    {
        "data": [
            {
                "date": "2019-1",
                "articles": [
                    {
                        "id": 1,
                        "title": "title1",
                        "date": "1"
                    },
                    {
                        "id": 2,
                        "title": "title2",
                        "date": "2"
                    },
                    {
                        "id": 4,
                        "title": "title3",
                        "date": "3"
                    }
                ]
            },
            {
                "date": "2019-2",
                "articles": [
                    {
                        "id": 5,
                        "title": "title5",
                        "date": "1"
                    },
                    {
                        "id": 6,
                        "title": "title6",
                        "date": "1"
                    },
                    {
                        "id": 7,
                        "title": "title7",
                        "date": "1"
                    }
                ]
            }
        ]})
"""
