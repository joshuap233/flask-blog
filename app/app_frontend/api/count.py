from .blueprint import api
from app.model.db import Post, Tag, Blog
from app.utils import generate_res


@api.route('/tags/posts/all')
def tags_posts_count_view():
    tags = Tag.visibility_tags().all()
    return generate_res(data=[{'id': tag.id, 'total': len(tag.posts.all())} for tag in tags])


# 获取所有文章id
@api.route('/posts/all')
def posts_all_view():
    posts = Post.visibility_posts()
    return generate_res(data=[post.id for post in posts])


@api.route('/posts/total')
def posts_count_view():
    total = Post.visibility_posts().total()
    return generate_res(data=total)


@api.route('/tags/total')
def tags_count_view():
    total = Tag.visibility_tags().total()
    return generate_res(data=total)


@api.route('/blog/total')
def blog_count_view():
    total = Blog.total()
    return generate_res(data=total)
