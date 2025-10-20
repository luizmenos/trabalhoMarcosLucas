import redis
import config
import base64
import os
from json import dumps


def redis_db(): 
    db = redis.Redis(
        host=os.getenv("REDIS_HOST", config.redis_host),
        port=config.redis_port,
        db=config.redis_db_number, 
        password= config.redis_password, 
        decode_responses=False
        )
    
    db.ping()
    
    return db

def redis_queue_push(db, message):
    
    db.lpush(config.redis_queue_name, message)
    
    
def main ():
    
    db = redis_db()
    
    input_dir = "input"

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            with open(os.path.join(input_dir, filename), "rb") as f:
                img_bytes = f.read()
                message = dumps({"filename": filename}).encode() + b"||" + img_bytes
                redis_queue_push(db, message)
                print(f"Enfileirada imagem: {filename}")
        
        
if __name__ == "__main__":
    main()