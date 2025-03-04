import redis
import json
import os

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = os.environ.get("REDIS_DB")
REDIS_PWD = os.environ.get("REDIS_PWD")

class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PWD):
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True  # 让返回值为字符串类型
            )
            # 测试连接
            self.redis_client.ping()
            print("成功连接到 Redis 服务器")
        except redis.ConnectionError:
            print("无法连接到 Redis 服务器")

    def add_key_value(self, key, value):
        try:
            value_json = json.dumps(value)
            result = self.redis_client.set(key, value_json)
            return result
        except Exception as e:
            print("添加键值对时发生错误", e)
            return False
        
    def get_value_by_key(self, key):
        try:
            value = self.redis_client.get(key)
            return json.loads(value)
        except Exception as e:
            print("查询键值对时发生错误", e)
            return None
        
    def delete_key(self, key):
        try:
            result = self.redis_client.delete(key)
            return result
        except Exception as e:
            print("删除键值对时发生错误", e)
            return 0
        
RedisClientInstance = RedisClient()