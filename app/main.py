import redis
import config
import uuid 
import datetime
import random
from json import dumps
from time import sleep

def redis_db(): 
    db = redis.Redis(host=config.redis_host, port=config.redis_port, db=config.redis_db_number, password= config.redis_password, decode_responses=True)
    
    db.ping()
    
    return db

def redis_queue_push(db, message):
    
    db.lpush(config.redis_queue_name, message)
    
    
def main (num_messages: int, delay: float = 1):
    
    db = redis_db()
    
    for i in range(num_messages):
        
        message=  {
            "id": str(uuid.uuid4()),
            "ts": datetime.utcnow().isoformat(),
            "data": {
                "message_number": i,
                "x": random.randrange(0, 100),
                "y": random.randrange(0, 100),
            },
        }
        
        message_json= dumps(message)
        
        print (f"Sending message {i+1} (id={message['id']})")
        redis_queue_push(db, message_json)
        
        sleep(delay)
        
        
if __name__ == "__main__":
    main(30, 0.1)