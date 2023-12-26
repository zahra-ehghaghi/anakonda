from redis import Redis
from .config import Config
from rq import Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from docker import from_env as docker_from_env
from sys import exit
from kubernetes import config
from pottery import Redlock
from time import time ,sleep
from threading import Thread
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
config.load_kube_config()

from .job import TaskJobController

lock= Redlock(key="anakonda_controller_lock", masters={re},auto_release_time=2)

def leader_watchdog():
    while True:
        re.expire("anakonda_controller_leader",1,xx=True)

    
def controller():   
    re.set(f"anakonda_controllers:{Config.NAME}",str(time()))     


    while True:
        if re.set("anakonda_controller_leader", Config.NAME, ex=1,nx=True) is True:
            print("I am leader.")
            break
        else:
            current_leader=re.get("anakonda_controller_leader")
            print(f"ّI am standby node, Current Leader is {current_leader}")
            sleep(1)
    lw=Thread(target=leader_watchdog,daemon=True)
    lw.start()
    for channel in Config.REDIS_CHANNELS.values():        
        pubsub.subscribe(channel) 
        print(f"subscribe to channel {channel}.")    
    for message in pubsub.listen():
        with lock:
            if message['type'] == "message":
                if message['channel'] == Config.REDIS_CHANNELS["NEW_TASKS"]:
                    print(f"Queueing new task with task_id={message['data']}")
                    queue.enqueue(TaskJobController.run_task,message["data"])

