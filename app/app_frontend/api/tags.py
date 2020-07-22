from app.utils import generate_res
from .blueprint import api
from app.model.db import Tag
from app.app_frontend.view_model import TagsView
from ..view_model import TagsQueryView


@api.route('/tags')
def tags_view():
    query = TagsQueryView()
    query_ = Tag.visibility_tags()
    tags = Tag.paging_search(**query.search_parameter, query=query_)
    return generate_res(data=TagsView(tags.items))
