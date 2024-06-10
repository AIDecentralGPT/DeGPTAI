from peewee import Model, CharField, BigIntegerField, AutoField
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional
from playhouse.shortcuts import model_to_dict
import time
import logging
import uuid  # 导入UUID模块生成唯一ID

log = logging.getLogger(__name__)

# 定义IpLog模型
class IpLog(Model):
    # id = CharField(primary_key=True, max_length=36)  # 使用字符串作为主键
    # user_id = CharField()  # 用户ID
    # ip_address = CharField()  # IP地址
    # created_at = BigIntegerField(default=lambda: int(time.time()))  # 创建时间
    id = AutoField()  # 使用AutoField作为主键
    user_id = CharField()  # 用户ID
    ip_address = CharField()  # 设备ID
    created_at = BigIntegerField(default=lambda: int(time.time()))  # 创建时间

    class Meta:
        database = DB  # 指定数据库
        # indexes = (
        #     (('ip_address',), True),  # 确保ip_address唯一
        # )
        table_name = 'ip_logs'  # 指定表名

# 定义Pydantic模型IpLogModel
class IpLogModel(BaseModel):
    id: Optional[int]  # 定义id字段为可选
    user_id: str  # 定义user_id字段，类型为字符串
    ip_address: str  # 定义device_id字段，类型为字符串
    created_at: int  # 定义created_at字段，类型为整数


# 定义IpLogsTable类，用于操作IpLogs表
class IpLogsTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([IpLog])  # 创建IpLog表

    # def insert_new_ip_log(self, user_id: str, ip_address: str) -> Optional[IpLogModel]:
    #     log.info(f"insert_new_ip_log插入新的IP日志")
    #     created_at = int(time.time())
    #     # 插入数据时不包含 id 字段
    #     ip_log = IpLog.create(user_id=user_id, ip_address=ip_address, created_at=created_at)
    #     # 从数据库获取插入的记录，确保包含自动生成的 id
    #     inserted_ip_log = IpLog.get(IpLog.id == ip_log.id)
    #     return IpLogModel(**model_to_dict(inserted_ip_log))


    def insert_new_ip_log(self, user_id: str, ip_address: str) -> Optional[IpLogModel]:
        log.info(f"Inserting new IP log for user_id: {user_id} with ip_address: {ip_address}")
        created_at = int(time.time())
        try:
            ip_log = IpLog.create(ip_address=ip_address, created_at=created_at,user_id=user_id)
            inserted_ip_log = IpLog.get(IpLog.id == ip_log.id)
            return IpLogModel(**model_to_dict(inserted_ip_log))
        except Exception as e:
            log.error(f"Error inserting IP log: {e}")
            return None


    # 根据ip_address获取IP日志
    def get_ip_log_by_address(self, ip_address: str) -> Optional[IpLogModel]:
        try:
            ip_log = IpLog.get(IpLog.ip_address == ip_address)  # 查询数据库中的IP日志
            return IpLogModel(**model_to_dict(ip_log))  # 将数据库对象转换为Pydantic模型并返回
        except IpLog.DoesNotExist:
            return None  # 如果查询失败，返回None

    # 更新IP日志信息
    def update_ip_log_by_address(self, ip_address: str, updated: dict) -> Optional[IpLogModel]:
        try:
            query = IpLog.update(**updated).where(IpLog.ip_address == ip_address)  # 更新IP日志信息
            query.execute()  # 执行更新操作
            ip_log = IpLog.get(IpLog.ip_address == ip_address)  # 查询更新后的IP日志
            return IpLogModel(**model_to_dict(ip_log))  # 将数据库对象转换为Pydantic模型并返回
        except IpLog.DoesNotExist:
            return None  # 如果更新失败，返回None

    # 删除IP日志信息
    def delete_ip_log_by_address(self, ip_address: str) -> bool:
        try:
            query = IpLog.delete().where(IpLog.ip_address == ip_address)  # 删除IP日志记录
            result = query.execute()  # 执行删除操作
            return result > 0  # 如果删除成功，返回True，否则返回False
        except:
            return False  # 如果出现异常，返回False

# 实例化IpLogsTable类
ip_logs_table = IpLogsTable(DB)
