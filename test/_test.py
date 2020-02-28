from flask import Flask
from flask_jwt_extended import create_access_token, JWTManager,decode_token

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = '1232131232'
jwt = JWTManager(app)

with app.app_context():
    token = create_access_token(identity=1, user_claims={'test': 'test'})
    res = decode_token(token)
    print(res)
