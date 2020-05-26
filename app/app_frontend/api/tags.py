from app.utils import generate_res
from .blueprint import api
from app.model.db import Tag, Visibility
from app.app_frontend.view_model import TagsView


@api.route('/tags')
def tags_view():
    tags = [
        tag for tag in Tag.query
        for post in tag.posts
        if post.visibility == Visibility.public.value
    ]
    return generate_res(data=TagsView(tags))
