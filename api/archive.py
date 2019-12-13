from .blueprint import api
from flask import jsonify


@api.route('/archive/')
def archive():
    return jsonify([
        {
            "date": "2019-1",
            "articles": [
                {
                    "id": 1,
                    "title": "title1",
                    "date": "1"
                },
                {
                    "id": 2,
                    "title": "title2",
                    "date": "2"
                },
                {
                    "id": 4,
                    "title": "title3",
                    "date": "3"
                }
            ]
        },
        {
            "date": "2019-2",
            "articles": [
                {
                    "id": 5,
                    "title": "title5",
                    "date": "1"
                },
                {
                    "id": 6,
                    "title": "title6",
                    "date": "1"
                },
                {
                    "id": 7,
                    "title": "title7",
                    "date": "1"
                }
            ]
        }
    ])
