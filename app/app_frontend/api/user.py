from app.model.db import User
from app.utils import generate_res
from .blueprint import api
from app.app_frontend.view_model import UserInfoView
from app.app_frontend.cache import cache


@api.route('/user/info')
@cache.cached()
def about():
    user = User.query.first()
    return generate_res(data=UserInfoView(user))
