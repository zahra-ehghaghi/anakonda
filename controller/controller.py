from redis import Redis
from .config import Config
re = re = Redis(host=Config.REDIS_HOST,
           port=Config.REDIS_PORT,
           username=Config.REDIS_USERNAME,
           password=Config.REDIS_PASSWORD,
           decode_responses=True)

pubsub= re.pubsub()
def controller():
    for channel in Config.REDIS_CHANNELS.values():
        pubsub.subscribe(channel)
        print(f"subscribe to channel {channel}.")
        for message in pubsub.listen():
            if message['type'] != "message":
                continue
            print (message)
