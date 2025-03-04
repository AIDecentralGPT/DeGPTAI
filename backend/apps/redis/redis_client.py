import redis
import json

from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PWD

class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PWD):
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True  # Make the return value a string type
            )
            # TEST CONNECTION
            self.redis_client.ping()
            print("Successfully connected to Redis server")
        except redis.ConnectionError:
            print("Unable to connect to Redis server")

    def add_key_value(self, key, value):
        try:
            value_json = json.dumps(value)
            result = self.redis_client.set(key, value_json)
            return result
        except Exception as e:
            print("An error occurred while adding a key value pair:", e)
            return False
        
    def get_value_by_key(self, key):
        try:
            value = self.redis_client.get(key)
            return json.loads(value)
        except Exception as e:
            print("Error occurred while querying key value pairs:", e)
            return None
        
    def delete_key(self, key):
        try:
            result = self.redis_client.delete(key)
            return result
        except Exception as e:
            print("An error occurred while deleting a key value pair:", e)
            return 0
        
RedisClientInstance = RedisClient()