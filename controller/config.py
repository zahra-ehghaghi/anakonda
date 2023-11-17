from os import environ


class Config:
    ENV = environ.get("ANAKONDA_CONTROLLER_ENV", "production")

    DEBUG = bool(int(environ.get("ANAKONDA_CONTROLLER_DEBUG", "0")))

    TESTING = DEBUG

    SECRET_KEY = environ.get("ANAKONDA_CONTROLLER_SECRET_KEY", "secretkey")

    SQLALCHEMY_DATABASE_URI = environ.get("ANAKONDA_CONTROLLER_DATABASE_URI", None)

    SQLALCHEMY_ECHO = DEBUG

    SQLALCHEMY_RECORD_QUERIES = DEBUG

    SQLALCHEMY_TRACK_MODIFICATIONS = DEBUG

    TIMEZONE = environ.get("ANAKONDA_CONTROLLER_TIMEZONE", "Europe/London")

    AVAILABLE_RUNTIMES = ["docker", "kubernetes"]

    REDIS_HOST=environ.get("ANAKONDA_CONTROLLER_REDIS_HOST", "localhost")
    
    REDIS_PORT=int(environ.get("ANAKONDA_CONTROLLER_REDIS_PORT", "6379"))
    
    REDIS_USERNAME=environ.get("ANAKONDA_CONTROLLER_REDIS_USERNAME", None)
    
    REDIS_PASSWORD=environ.get("ANAKONDA_CONTROLLER_REDIS_PASSWORD", None)
    
    REDIS_CHANNELS ={"NEW_TASKS": "anakonda-new-task",}
    