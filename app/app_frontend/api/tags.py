from app.utils import generate_res
from .blueprint import api
from app.model.db import Tag
from app.app_frontend.view_model import TagsView
from app.cache import cache


@api.route('/tags')
@cache.cached()
def tags_view():
    tags = Tag.get_visibility_tag()
    return generate_res(data=TagsView(tags))
