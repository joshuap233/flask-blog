import os

import requests

from app.utils import generate_res
from .blueprint import admin
from ..token_manager import login_required


@admin.route('/frontend/rebuild')
@login_required
def rebuild():
    res = requests.get(os.getenv('rebuild_api'))
    if res.status_code != 200:
        return generate_res(status='failed')
    return generate_res()
