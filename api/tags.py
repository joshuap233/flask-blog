from .blueprint import api
from flask import jsonify


@api.route('/tags/')
def tags():
    return jsonify([
        {
            "name": "ubuntu",
            "article": [
                {
                    "id": 1,
                    "title": "title1"
                },
                {
                    "id": 2,
                    "title": "title2"
                },
                {
                    "id": 3,
                    "title": "title3"
                }
            ]
        },
        {
            "name": "linux",
            "article": [
                {
                    "id": 4,
                    "title": "title4"
                },
                {
                    "id": 5,
                    "title": "title5"
                },
                {
                    "id": 6,
                    "title": "title6"
                }
            ]
        }
    ])
