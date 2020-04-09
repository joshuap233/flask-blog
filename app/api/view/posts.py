from app.utils import generate_res
from .blueprint import api


# @api.route('/posts')
# def posts():
#     query = QueryView()
#     pagination = Post.search(**query.search_parameter)
#     return generate_res("success", data=[{
#         'id': post.id,
#         'title': post.title,
#         # TODO :返回article简介(图片加载问题)
#         'article': post.article
#     } for post in pagination.items])


@api.route('/posts')
def posts():
    data = {
        'current_page': '1',
        'content': [{
            "id": 1,
            "title": 'article title行行还行还行还行还行还行行还行还行还行还行还行',
            "excerpt": '  进程: 进程是一个实体。每个进程都有自己的地址空间(CPU分配) 是具有一定独立功能的程序关于某个数据集合上的一次运行活动,进程是系统进行资源分配和调度的一个独立单位. 线程: 线程是进程中的一个实体 一个进程内部可能包含了很多顺序执行流，每个顺序执行流就是一个线程 应用场景: 多进程:cpu密集型 多线程:io密集型',
            "change_date": " 2019/10/2 12:50",
            "comments": 0
        }, {
            "id": 2,
            "title": 'article title行行还行还行还行还行还行',
            "excerpt": '  进程: 进程是一个实体。每个进程都有自己的地址空间(CPU分配) 是具有一定独立功能的程序关于某个数据集合上的一次运行活动,进程是系统进行资源分配和调度的一个独立单位. 线程: 线程是进程中的一个实体 一个进程内部可能包含了很多顺序执行流，每个顺序执行流就是一个线程 应用场景: 多进程:cpu密集型 多线程:io密集型',
            "change_date": " 2019/10/2 12:50",
            "comments": 0

        }, {
            "id": 3,
            "title": 'article title行还行还行还行还行',
            "excerpt": '  进程: 进程是一个实体。每个进程都有自己的地址空间(CPU分配) 是具有一定独立功能的程序关于某个数据集合上的一次运行活动,进程是系统进行资源分配和调度的一个独立单位. 线程: 线程是进程中的一个实体 一个进程内部可能包含了很多顺序执行流，每个顺序执行流就是一个线程 应用场景: 多进程:cpu密集型 多线程:io密集型',
            "change_date": " 2019/10/2 12:50",
            "comments": 0

        }, {
            "id": 4,
            "title": 'article title',
            "excerpt": '  进程: 进程是一个实体。每个进程都有自己的地址空间(CPU分配) 是具有一定独立功能的程序关于某个数据集合上的一次运行活动,进程是系统进行资源分配和调度的一个独立单位. 线程: 线程是进程中的一个实体 一个进程内部可能包含了很多顺序执行流，每个顺序执行流就是一个线程 应用场景: 多进程:cpu密集型 多线程:io密集型',
            "change_date": " 2019/10/2 12:50",
            "comments": 0

        }]}
    return generate_res("success", data=data)
