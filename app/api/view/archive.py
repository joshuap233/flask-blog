from time import strftime, localtime

from .blueprint import api
from app.database import Post
from app.utils import generate_res


@api.route('/archive/<int:page>/')
def archive(page):
    # per_page 写入config
    pagination = Post.query.order_by(Post.create_date.desc()).paginate(page=page, per_page=10, error_out=False)
    posts = pagination.items
    data = []
    for post in posts:
        timestamp = post.create_date / 1000
        year, month, date = strftime('%Y-%m-%d', localtime(timestamp)).split("-")
        article = {"id": post.id, "title": post.title, "date": date}
        if len(data) == 0:
            data.append({"date": f'{year}-{month}', "articles": [article]})
            continue
        for item in data:
            if item.get('date') == f'{year}-{month}':
                item["articles"].append(article)
            else:
                data.append({"date": f'{year}-{month}', "articles": [article]})
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
