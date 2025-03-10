from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from peewee import *  # 导入Peewee中的所有模块
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from apps.web.internal.db import DB  # 导入数据库实例DB
from typing import List, Union, Optional
from datetime import datetime, date
import time
import uuid

# 定义RewardDate模型
class RewardDate(Model):
    id = CharField(unique=True)  # 定义唯一的字符字段id
    name = CharField()  # 定义字符字段name
    start_time = CharField() # 定义字符字段start_time
    end_time = CharField(null=True) # 定义字符字段end_time
    open = CharField(null=False) # 定义字符字段open
    updated_at = BigIntegerField()  # 定义大整数字段updated_at
    created_at = BigIntegerField()  # 定义大整数字段created_at

    class Meta:
        database = DB  # 指定数据库

class RewardDateModel(BaseModel):
    id: str # 主键
    name: str # 名称
    start_time: datetime  # 开始时间
    end_time: datetime # 结束使劲按
    open: Optional[bool] = False # 是否开启
    created_at: int # 创建时间
    updated_at: int # 更新时间

# 定义RewardDate创建更新实体
class RewardDateRequest(BaseModel):
    name: str
    start_time: str
    end_time: str

# 定义RewardDateTable类，用于操作RewardDate表
class RewardDateTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([RewardDate])  # 创建RewardDate表

    # 插入奖励区间维护
    def insert(
        self,
        rewarddate: RewardDateRequest
    ) -> Optional[RewardDateModel]:
        
        try:
            rewarddate = RewardDateModel(
                id = str(uuid.uuid4()),
                name = rewarddate.name,
                start_time = rewarddate.start_time,
                end_time =  rewarddate.end_time,
                open = False,
                created_at = int(time.time()),
                updated_at = int(time.time())
            )
            RewardDate.create(**rewarddate.model_dump())
            return True
        except Exception as e:
            print("====================", e)
            return False

    # 获取奖励区间信息根据ID
    def getById(self, id: str) -> Optional[List[RewardDateModel]]:
        try:
            rewarddata = RewardDate.get_or_none(RewardDate.id == id)
            if rewarddata is None:
                return None
            else:
                rewarddata_dict = model_to_dict(rewarddata)  # 将数据库对象转换为字典
                rewarddata_model = RewardDateModel(**rewarddata_dict)  # 将字典转换为Pydantic模型
                return rewarddata_model
        except:
            return None  

    # 获取奖励区间信息列表
    def page(self, skip: int = 0, limit: int = 10, search: str = "", status: str = "") -> Optional[List[RewardDateModel]]:
        try:
            query = RewardDate.select()
            # 名称筛选
            if search:
                query = query.where(RewardDate.name.contains(search))
            # 状态筛选
            if status:
                open = True if status == "open" else False
                query = query.where(RewardDate.open == open)

            # 获取总记录数
            total = query.count()

            # 将数据库对象转换为字典
            # 获取当前页的记录
            rewarddata_list = [
                RewardDateModel(**model_to_dict(rewarddate))
                for rewarddate in query.limit(limit).offset((skip - 1)*limit).order_by(RewardDate.start_time.desc())  # 限制查询结果的数量和偏移量
            ]
            # 返回结果
            return {'total': total, 'data': rewarddata_list}
        except:
            return None

    # 更新奖励区间维护
    def update(self, id: str, name: str, start_time: str, end_time: str) -> bool:
        try:
            update = RewardDate.update(name=name, start_time=start_time, end_time=end_time, updated_at=int(time.time())).where(RewardDate.id==id)
            update.execute()
            return True
        except Exception as e:
            return False
      
    # 开启奖励区间维护
    def updateStatus(self, id: str) -> bool:
        try:
            rewarddata = RewardDate.get_or_none(RewardDate.id == id)
            if rewarddata is not None:
                rewarddata_dict = model_to_dict(rewarddata)
                rewarddata_model = RewardDateModel(**rewarddata_dict)
                status = not rewarddata_model.open
                update = RewardDate.update(open=False, updated_at=int(time.time())).where(RewardDate.open==True)
                update.execute()
                update = RewardDate.update(open=status, updated_at=int(time.time())).where(RewardDate.id==id)
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
            delete = RewardDate.delete_by_id(RewardDate.id==id)
            delete.execute()
            return True
        except Exception as e:
            return False
        

    # 获取当前开启的奖励
    def get_current_open(self) -> bool:
        try:
            rewarddata = RewardDate.get_or_none(RewardDate.open == True)
            if rewarddata is None:
                return None
            else:
                rewarddata_dict = model_to_dict(rewarddata)  # 将数据库对象转换为字典
                rewarddata_model = RewardDateModel(**rewarddata_dict)  # 将字典转换为Pydantic模型
                return rewarddata_model
        except:
            return None 
        
# 初始化 Rewards 表
RewardDateTableInstance = RewardDateTable(DB)