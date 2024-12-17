from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from peewee import *  # 导入Peewee中的所有模块
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from typing import List, Union, Optional  # 导入类型提示

import uuid
import time  # 导入time模块

from apps.web.internal.db import DB, aspect_database_operations  # 导入数据库实例DB


####################
# ErrorLog DB Schema
####################

# 定义ErrorLog模型
class ErrorLog(Model):
    id = CharField(unique=True)  # 定义唯一的字符字段id
    name = CharField()  # 名称
    err = TextField()  # 错误信息
    created_at = BigIntegerField()  # 定义大整数字段created_at
    updated_at = BigIntegerField()  # 定义大整数字段updated_at

    class Meta:
        database = DB  # 指定数据库
        table_name = 'error_log'  # 指定表名

# 定义Pydantic模型ErrorLog
class ErrorLogModel(BaseModel):
    id: str  # 定义id字段，类型为字符串
    name: str  # 定义名称字段，类型为字符串
    err: str  # 定义错误信息字段，类型为字符串
    created_at: int  # 定义created_at字段，类型为整型，表示epoch时间戳
    updated_at: int  # 定义updated_at字段，类型为整型，表示epoch时间戳

# 定义Pydantic模型ErrorLog
class ErrorLogRequest(BaseModel):
    name: str  # 定义名称字段，类型为字符串
    err: str  # 定义错误信息字段，类型为字符串


# 定义ErrorLogTable类，用于操作ErrorLog表
class ErrorLogTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([ErrorLog])  # 创建ErrorLog表

    # 插入新用户
    def insert_errorlog(
        self,
        name: str,
        err: str
    ) -> Optional[ErrorLogModel]:
        
        # 创建UserModel实例
        errLog = ErrorLogModel(
            **{
                "id": str(uuid.uuid4()),
                "name": name,
                "err": err,
                "created_at": int(time.time()),
                "updated_at": int(time.time())
            }
        )

        # 在数据库中创建新日志
        result = ErrorLog.create(**errLog.model_dump())
        
        # return result info:
        return result  # 返回创建的日志

# 实例化ErrorLogTable类
ErrorLogInstance = ErrorLogTable(DB)
