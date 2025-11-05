from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from peewee import *  # 导入Peewee中的所有模块
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from apps.web.internal.db import DB  # 导入数据库实例DB
from apps.web.util.apiutils import ApiUtilInstance
from typing import List, Union, Optional
from datetime import datetime, date
import time
import uuid

# 定义ApiKey模型
class ApiKey(Model):
    id = CharField(unique=True)  # 定义唯一的字符字段id
    key = CharField()  # 定义字符字段key
    store_val = CharField()  # 对用户KEY值
    open = CharField(null=False) # 定义字符字段open
    created_at = BigIntegerField()  # 定义大整数字段created_at
    updated_at = BigIntegerField()  # 定义大整数字段updated_at

    class Meta:
        database = DB  # 指定数据库

class ApiKeyModel(BaseModel):
    id: str # 主键
    key: str # key
    store_val: str # key加密
    open: Optional[bool] = False # 是否开启
    created_at: int # 创建时间
    updated_at: int # 更新时间

# 定义ApiKey创建更新实体
class ApiKeyRequest(BaseModel):
    key: str

# 定义ApiKeyTable类，用于操作ApiKey表
class ApiKeyTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([ApiKey])  # 创建ApiKey表

    # 插入奖励区间维护
    def insert(self) -> Optional[ApiKeyRequest]:
        key, stored_value = ApiUtilInstance.generate_key_with_hash()
        try:
            rewarddate = ApiKeyModel(
                id = str(uuid.uuid4()),
                key = key,
                store_val= stored_value,
                open = False,
                created_at = int(time.time()),
                updated_at = int(time.time())
            )
            ApiKey.create(**rewarddate.model_dump())
            return True
        except Exception as e:
            print("====================", e)
            return False

    # 获取奖励区间信息根据key
    def getByKey(self, store_val: str) -> Optional[List[ApiKeyModel]]:
        try:
            apikey = ApiKey.get_or_none(ApiKey.store_val == store_val)
            if apikey is None:
                return None
            else:
                apikey_dict = model_to_dict(apikey)  # 将数据库对象转换为字典
                apikey_model = ApiKeyModel(**apikey_dict)  # 将字典转换为Pydantic模型
                return apikey_model
        except:
            return None  

    # 获取奖励区间信息列表
    def page(self, skip: int = 0, limit: int = 10, search: str = "", status: str = "") -> Optional[List[ApiKeyModel]]:
        try:
            query = ApiKey.select()
            # 名称筛选
            if search:
                query = query.where(ApiKey.key.contains(search))
            # 状态筛选
            if status:
                open = True if status == "open" else False
                query = query.where(ApiKey.open == open)

            # 获取总记录数
            total = query.count()

            # 将数据库对象转换为字典
            # 获取当前页的记录
            apikey_list = [
                ApiKeyModel(**model_to_dict(apikey))
                for apikey in query.limit(limit).offset((skip - 1)*limit).order_by(ApiKey.created_at.desc())  # 限制查询结果的数量和偏移量
            ]
            # 返回结果
            return {'total': total, 'data': apikey_list}
        except:
            return None
      
    # 开启奖励区间维护
    def updateStatus(self, id: str) -> bool:
        try:
            apikey = ApiKey.get_or_none(ApiKey.id == id)
            if apikey is not None:
                apikey_dict = model_to_dict(apikey)
                apikey_model = ApiKeyModel(**apikey_dict)
                status = not apikey_model.open
                update = ApiKey.update(open=status, updated_at=int(time.time())).where(ApiKey.id==id)
                update.execute()
                return True
            else:
                return False
        except Exception as e:
            print("======================", e)
            return False
      
    # 删除奖励区间维护
    def delete(self, id: str) -> bool:
        try:
            delete = ApiKey.delete_by_id(ApiKey.id==id)
            delete.execute()
            return True
        except Exception as e:
            return False
        
# 初始化 ApiKey 表
ApiKeyTableInstance = ApiKeyTable(DB)