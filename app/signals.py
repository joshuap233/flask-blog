from blinker import Namespace
from app.cache import cache

signals = Namespace()

cache_signals = signals.signal('cache_signals')
email_signals = signals.signal('email_signals')

SIGNAL_SENDER = {
    'changeUserInfo': 'changeUserInfo',
    'modifyPosts': 'modifyPosts',
    'deletePost': 'deletePost',
    'modifyTags': 'modifyTags',
    'deleteTags': 'deleteTags'
}


def delete_user_info_cache(_):
    cache.delete('view//api/user/info')


def modify_post_cache(_, pid):
    cache.delete_many(f'view//api/post/{pid}', 'view//api/posts', 'view//api/tags')


def delete_post_cache(_):
    cache.delete_many('view//api/posts', 'view//api/tags')


def modify_tags_cache(_):
    cache.delete('view//api/tags')


def delete_tags_cache(_):
    cache.delete('view//api/tags')


def register_signal():
    cache_signals.connect_via(SIGNAL_SENDER['changeUserInfo'])(delete_user_info_cache)
    cache_signals.connect_via(SIGNAL_SENDER['modifyPosts'])(modify_post_cache)
    cache_signals.connect_via(SIGNAL_SENDER['deletePost'])(delete_post_cache)
    cache_signals.connect_via(SIGNAL_SENDER['modifyTags'])(modify_tags_cache)
    cache_signals.connect_via(SIGNAL_SENDER['deleteTags'])(delete_tags_cache)
