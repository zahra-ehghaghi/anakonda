from flask import Blueprint, Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from .config import Config

db = SQLAlchemy()
mg = Migrate()
ma = Marshmallow()
print (Config.REDIS_CONFIG)
re = Redis(host=Config.REDIS_CONFIG[3],
           port=Config.REDIS_CONFIG[4],
           username=Config.REDIS_CONFIG[1] if Config.REDIS_CONFIG[1] !=  "none" else  None,
           password=Config.REDIS_CONFIG[2] if Config.REDIS_CONFIG[1] !=  "none" else  None,
           db=Config.REDIS_CONFIG[5])
apiv1_bp = Blueprint("apiv1_bp", __name__, url_prefix="/api/v1")
apiv1 = Api(apiv1_bp)

from . import resource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mg.init_app(app, db)
    ma.init_app(app)
    app.register_blueprint(apiv1_bp)
    return app
