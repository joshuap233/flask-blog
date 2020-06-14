import pytest
from app.app_admin import create_admin_app
from app.model.baseDB import db as _db


@pytest.fixture(scope="session")
def app(request):
    app = create_admin_app(env="testing")
    with app.app_context():
        _db.drop_all()
        _db.create_all()
    return app
