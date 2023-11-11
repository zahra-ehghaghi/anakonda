from os import environ
from re import match

class Config:
    ENV = environ.get("ANAKONDA_API_ENV", "production")

    DEBUG = bool(int(environ.get("ANAKONDA_API_DEBUG", "0")))

    TESTING = DEBUG

    SECRET_KEY = environ.get("ANAKONDA_API_SECRET_KEY", "secretkey")

    JSONIFY_PRETTYPRINT_REGULAR = bool(
        int(environ.get("ANAKONDA_API_JSON_PRETTYPRINT", "0"))
    )

    SQLALCHEMY_DATABASE_URI = environ.get("ANAKONDA_API_DATABASE_URI", None)

    SQLALCHEMY_ECHO = DEBUG

    SQLALCHEMY_RECORD_QUERIES = DEBUG

    SQLALCHEMY_TRACK_MODIFICATIONS = DEBUG

    TIMEZONE = environ.get("ANAKONDA_API_TIMEZONE", "Europe/London")

    AVAILABLE_RUNTIMES = ["docker", "kubernetes"]

    REDIS_CONFIG = match(
        "^(.*):(.*)\@(.+):([1-9]+[0-9]*)\/([0-9]|10|11|12|13|14|15)$",
        environ.get("ANAKONDA_API_REDIS_URI", "")
    )