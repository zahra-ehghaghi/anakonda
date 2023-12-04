from time import sleep
from redis import Redis
from .config import Config
from rq import Queue
import sqlalchemy
re = Redis(host=Config.REDIS_HOST,
           port=Config.REDIS_PORT,
           username=Config.REDIS_USERNAME,
           password=Config.REDIS_PASSWORD,
           decode_responses=True)
queue = Queue(connection= re)
pubsub= re.pubsub()
db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI).connect()
metadata = sqlalchemy.MetaData()
tasks_table = sqlalchemy.Table("tasks",metadata,autoload_with=db)


def controller():
    for channel in Config.REDIS_CHANNELS.values():
        pubsub.subscribe(channel)
        print(f"subscribe to channel {channel}.")
        for message in pubsub.listen():
            if message['type'] == "message":
                if message['channel'] == Config.REDIS_CHANNELS["NEW_TASKS"]:
                    queue.enqueue(do_new_task,message['data'])

def do_new_task(task_id):
   task_find_query =  tasks_table.select().where(tasks_table.c.id == task_id)
   task = db.execute(task_find_query).first()
   if task != None:
       print(task[1])
       task_update_query = tasks_table.update().where(tasks_table.c.id == task_id).values(status="processing")
       db.execute(task_update_query)
       db.commit()
              
       # do the actual job.
       sleep(10)

       task_update_query = tasks_table.update().where(tasks_table.c.id == task_id).values(status="success")
       db.execute(task_update_query)
       db.commit()
       
       