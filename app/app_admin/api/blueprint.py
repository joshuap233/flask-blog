from app.myFlask import MyBlueprint

admin = MyBlueprint(
    'admin',
    __name__,
    url_prefix='/api',
)
