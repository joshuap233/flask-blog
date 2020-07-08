import random
from faker import Faker
from flask import url_for
from .data import user_info, headers

faker = Faker('zh_CN')

TAG_QUERY = {
    'page': 0,
    'pageSize': 10,
}

TAG = {
    'id': 1,
    'name': 'tags1',
    'describe': 'describe',
}
TAGS = []


def test_login(client):
    client.post(
        url_for('admin.register_view'),
        json=user_info
    )
    res = client.post(
        url_for('admin.login_view'),
        json=user_info
    )
    data = res.get_json().get('data')
    headers['identify'] = data.get('id')
    headers['Authorization'] = f'Bearer {data.get("token")}'


class Test_tags_view:
    # 测试带参查询
    def test_tags_get(self, client):
        res = client.get(url_for('admin.tags_view'), headers=headers)
        assert b'success' in res.data
        global TAGS
        global TAG
        TAGS.extend(res.get_json()['data']['values'])
        TAG = TAGS[0]
        assert len(TAGS) != 0

    def test_get_all_tags(self, client):
        # 该接口用于前端标签名自动提示
        res = client.get(url_for('admin.all_tags_view'), headers=headers)
        assert b'success' in res.data

    # 添加标签
    def test_tags_post(self, client):
        res = client.post(url_for('admin.tags_view'), headers=headers)
        tid = res.get_json()['data']['id']
        assert b'success' in res.data
        res = client.put(url_for('admin.tags_view', tid=tid), headers=headers, json={
            'name': str(random.randint(0, 1000)),
            'describe': 'describe123'
        })
        assert b'success' in res.data

    # 修改标签名
    def test_tags_put(self, client):
        tag = TAGS[0]
        tag['name'] = 'tags222' + str(random.randint(1, 10000))
        res = client.put(url_for('admin.tags_view', tid=tag['id']), headers=headers, json=tag)
        assert b'success' in res.data

        # 测试标签名重复的情况
        tag['name'] = 'tags2'
        res = client.put(url_for('admin.tags_view', tid=tag['id']), headers=headers, json=tag)
        assert b'failed' in res.data

    def test_upload_tag_img(self, client):
        # f = open(os.getenv('TEST_PIC_PATH'), "rb")
        import io
        res = client.post(
            url_for('admin.images_upload_view', source='tags', source_id=TAG['id']),
            data={'image': (io.BytesIO(b"my tag images"), 'tag1.jpg')},
            content_type='multipart/form-data',
            headers=headers
        )
        assert b'success' in res.data

    def test_img_get(self, client):
        pass
        # res = client.get(
        #     url_for('admin.tags_pic_view', **{'tag_name': 'test'}),
        #     headers=HEADERS
        # )

    def test_tags_delete(self, client):
        res = client.delete(url_for('admin.tags_view'), headers=headers, json={'id_list': [TAGS[0]['id']]})
        assert b'success' in res.data

        # 确认是否删除成功
        res = client.delete(url_for('admin.tags_view'), headers=headers, json={'id_list': [TAGS[0]['id']]})
        assert b'failed' in res.data
