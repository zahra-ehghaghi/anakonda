from redis import Redis
from .config import Config
from rq import Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from system import exit




re = Redis(host=Config.REDIS_HOST,
           port=Config.REDIS_PORT,
           username=Config.REDIS_USERNAME,
           password=Config.REDIS_PASSWORD,
           decode_responses=True)
pubsub= re.pubsub()
queue = Queue(connection= re)
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
mapper = automap_base()
mapper.prepare(autoload_with=engine)
db = Session(engine)
docker = docker_from_env()
if docker.ping() is False:
    exit(1)


from .job import TaskJobController


def controller():
    for channel in Config.REDIS_CHANNELS.values():
        pubsub.subscribe(channel)
        print(f"subscribe to channel {channel}.")
        for message in pubsub.listen():
            if message['type'] == "message":
                if message['channel'] == Config.REDIS_CHANNELS["NEW_TASKS"]:
                    queue.enqueue(TaskJobController.run_task,message["data"])