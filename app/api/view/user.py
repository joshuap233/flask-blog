from .blueprint import api
from app.database import User
from app.utils import generate_res


@api.route('/user/about/')
def about():
    user = User.query.first().user_about
    return generate_res("success", "user_about", data=user)
