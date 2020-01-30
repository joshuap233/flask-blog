from .blueprint import api
from app.model.db import Post
from app.utils import generate_res


@api.route('/posts/<int:post_id>/')
def posts(post_id):
    post = Post.query.get(post_id)
    article = {
        "id": post.id,
        "title": post.title,
        "contents": post.contents
    }
    return generate_res("success", data=article)


""" 
    state:"success",
    msg: "post"
    article:{
        "id": 1,
        "title": "并发编程",
        "contents": "# 进程 线程\n进程:\n进程是一个实体。每个进程都有自己的地址空间(CPU分配)\n是具有一定独立功能的程序关于某个数据集合上的一次运行活动,进程是系统进行资源分配和调度的一个独立单位.\n线程:\n线程是进程中的一个实体\n一个进程内部可能包含了很多顺序执行流，每个顺序执行流就是一个线程\n\n应用场景:\n多进程:cpu密集型\n多线程:io密集型\n\n# 协程\n协程，又称微线程\n协程是一种比线程更加轻量级的存在，最重要的是，协程不被操作系统内核管理，协程是完全由程序控制的。\n不像线程切换需要花费操作系统的开销,线程数量越多，协程的优势就越明显。\n协程不需要多线程的锁机制，因为只有一个线程，不存在变量冲突。\n\n\n# 阻塞 \n阻塞调用是指调用结果返回之前，当前线程会被挂起，一直处于等待消息通知，不能够执行其他业务。函数只有在得到结果之后才会返回。\n\n常见的有网络IO阻塞, 磁盘IO阻塞,用户输入阻塞 \n\n  \n# 非阻塞\n程序在等待某操作过程中，自身不被阻塞，可以继续运行干别的事情，则称该程序在该操作上是非阻塞的。\n非阻塞指在不能立刻得到结果之前，该函数不会阻塞当前线程，而会立刻返回\n \n# 同步\n同步:一个任务的完成需要依赖另外一个任务时，只有等待被依赖的任务完成后，依赖的任务才能算完成，这是一种可靠的任务序列。要么成功都成功，失败都失败，两个任务的状态可以保持一致。\n\n# 异步\n\n异步: 异步是不需要等待被依赖的任务完成，只是通知被依赖的任务要完成什么工作，依赖的任务也立即执行，只要自己完成了整个任务就算完成了。至于被依赖的任务最终是否真正完成，依赖它的任务无法确定，所以它是不可靠的任务序列。\n\n同步 阻塞\n```python\nimport requests\ndef test1():\n    print('--------开始请求url1----------')\n    requests.get(URL1)\n    print('--------开始请求url1----------')  # 阻塞\n    requests.get(URL2)\ntest1()\n```\n\n\n线程异步 非阻塞\n```python\nimport requests\nimport threading\ndef test2():\n    def request(url):\n        t = threading.Thread(target=lambda _: requests.get(_), args=(url,))\n        t.start()\n        return t\n    print('开始请求url:', URL1)\n    request(URL1)                         \n    print('开始请求url:', URL2)     # 非阻塞\n    request(URL2)\ntest2()\n```\n\n\n协程异步 非阻塞\n```python\nimport asyncio\nimport aiohttp\ndef test3():\n    async def request(url):          #async 定义协程\n        print('开始请求:', url)\n        async with aiohttp.ClientSession() as session:\n            await session.get(url)   # await 后是可等待对象                       \n    task = [asyncio.ensure_future(request(_)) for _ in [URL1, URL2]]     \n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(asyncio.wait(task))\ntest3()\n```\n\n\n同步请求\n```python\ndef test4():\n    start = time.time()\n    url = 'https://shushugo.com/'\n    for _ in range(10):\n        result = requests.get(url)\n        print(result)\n    end = time.time()\n    print('用时:', end - start):\n```\n\n\n\n异步请求\n```python\ndef test5():\n    start = time.time()\n\n    async def get(url):\n        async with aiohttp.ClientSession() as session:\n            response = await session.get(url)\n        return response\n\n    async def request():\n        url = 'https://shushugo.com/'\n        print('正在等待', url)\n        result = await get(url)\n        print('结果:', result)\n\n    tasks = [asyncio.ensure_future(request()) for _ in range(10)]\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(asyncio.wait(tasks))\n\n    end = time.time()\n    print('用时:', end - start)\n\n```\n"
    })
"""
