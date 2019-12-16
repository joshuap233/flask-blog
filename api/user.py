from .blueprint import api
from ..database import User
from ..utils import generate_res


@api.route('/user/about/')
def about():
    user = User.query.first().user_about
    return generate_res("success", "user_about", data=user)
