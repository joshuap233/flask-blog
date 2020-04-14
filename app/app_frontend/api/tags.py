from app.utils import generate_res
from .blueprint import api
from flask import url_for, current_app, send_from_directory
from app.shared.model.db import Tag
from app.shared.model.view_model import QueryView


@api.route('/tags')
def tags_view():
    query = QueryView(order_by=False)
    pagination = Tag.paging_search(**query.search_parameter)
    return generate_res(data={
        "page": query.page,
        "content": [{
            "id": tag.id,
            "name": tag.name,
            "count": tag.count,
            "describe": tag.describe,
            "image": {
                "url": url_for('api.send_images_view', filename='1.png', _external=True)
            }
        } for tag in pagination.items if len(tag.posts.all())]
    })


@api.route('/tags/all')
def all_tags_view():
    return generate_res(data=[{
        tag.id: tag.name
    } for tag in Tag.query.all()])
