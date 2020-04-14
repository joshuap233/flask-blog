from app.utils import generate_res
from .blueprint import api
from app.model.view_model import QueryView
from app.model.db import Post


@api.route('/posts/')
def posts_view():
    query = QueryView(order_by=False)
    tid = query.filters.get('tid')
    posts = Post.paging_by_tid(
        tid, **query.search_parameter) if tid else Post.paging_search(
        **query.search_parameter
    )
    return generate_res("success", data={
        'page': query.page,
        'content': [{
            'id': post.id,
            'title': post.title,
            'excerpt': post.excerpt_html,
            'change_date': post.change_date,
            'comments': post.comments,
            'tags': [{
                'id': tag.id,
                'name': tag.name
            } for tag in post.tags]
        } for post in posts.items]
    })
