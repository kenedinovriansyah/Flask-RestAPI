import logging
import json
from pusher import Pusher
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from flask_cors import CORS
from flask_restless import APIManager
from flask_restplus import Api
from flask_mail import Mail

db = SQLAlchemy()
guard = Praetorian()
cors = CORS()
pusher = Pusher(
    app_id='896313',
    key='7b28509430ddfeee7814',
    secret='374328196db97c6e74ed',
    cluster='ap1',
    ssl=True
)
apimanager = APIManager()
mail = Mail()
from app.component.user.views import ns as user
from app.component.restAPI.views import ns as restAPI

blueprint = Blueprint('api',__name__,url_prefix='/api')
api = Api(blueprint,doc='access')
api.add_namespace(user)
api.add_namespace(restAPI)

import app.database.models
from app.database.models import User

def config_extension(index):
    logging.getLogger('flask_cors').level = logging.DEBUG
    logging.basicConfig(level=logging.INFO)

    with index.app_context():
        db.init_app(index)
        guard.init_app(index,User)
        cors.init_app(index,resources={r"/api/*": {"origins": "*"}},supports_credentials=True)
        apimanager.init_app(index,flask_sqlalchemy_db=db)
        apimanager.create_api(User)
        mail.init_app(index)
        index.register_blueprint(blueprint)