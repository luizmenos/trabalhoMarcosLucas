import redis
import config
import base64
import os
from io import BytesIO
from PIL import Image

def redis_db(): 
    db = redis.Redis(
        host=os.getenv("REDIS_HOST", config.redis_host),
        port=config.redis_port, 
        db=config.redis_db_number, 
        password= os.getenv("REDIS_PASSWORD", config.redis_password), 
        decode_responses=False
        )
    
    db.ping()
    
    return db

def redis_queue_push(db, message):
    
    db.lpush(config.redis_queue_name, message)

def redis_queue_pop(db):

    _, message_json = db.brpop(config.redis_queue_name)

    return message_json

def process_image(message, db):
    try: 
        filename, img_bytes = message.split(b"||", 1)
        filename = eval(filename.decode())["filename"]

        image = Image.open(BytesIO(img_bytes))

        image = image.convert("L") # conversão para escala de cinza
        os.makedirs("output", exist_ok=True)
        out_path = os.path.join("output", f"processed_{filename}")
        image.save(out_path)
        print(f"Processada e salva: {out_path}", flush=True)
    except Exception as e:
        print(f"Falha ao processar {filename}: {e}. Reeinfileirando...", flush=True)
        db.lpush(config.redis_queue_name, message) 



def main():

    db = redis_db()
    # print("Worker: Conectado ao Redis. Aguardando mensagens...", flush=True)
    while True:        
        message = redis_queue_pop(db)
        # print(f"Worker: Mensagem recebida da fila. Tamanho: {len(message)} bytes.", flush=True) 
        process_image(message, db)
        


        
if __name__ == "__main__":
    main()