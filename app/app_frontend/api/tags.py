from app.utils import generate_res
from .blueprint import api
from flask import url_for
from app.model.db import Tag, Visibility


@api.route('/tags')
def tags_view():
    tags = [
        tag for tag in Tag.query
        for post in tag.posts
        if post.visibility == Visibility.public.value
    ]
    return generate_res(data={
        "content": [{
            "id": tag.id,
            "name": tag.name,
            "count": tag.count,
            "describe": tag.describe,
            "image": {
                "url": url_for('api.send_images_view', filename=tag.link.url, _external=True) if tag.link else ''
            }
        } for tag in tags]
    })
