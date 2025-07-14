<<<<<<< HEAD
# Import the required modules
from peewee import Model, CharField, AutoField, ForeignKeyField, BigIntegerField
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional
from apps.web.models.users import User
from playhouse.shortcuts import model_to_dict
=======
# 导入所需模块
from peewee import Model, CharField, AutoField, ForeignKeyField, BigIntegerField
from apps.web.internal.db import DB  # 导入数据库实例DB
from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from typing import Optional  # 导入类型提示
from apps.web.models.users import User  # 导入User模型
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
>>>>>>> fingerprintAuth-out
import time
import logging
log = logging.getLogger(__name__)

<<<<<<< HEAD
# Define Device Model
class Device(Model):
    id = AutoField()  # Using AutoField as the primary key
    user_id = CharField()  # user id
    device_id = CharField()  # device ID
    created_at = BigIntegerField(default=lambda: int(time.time()))  # Creation time

    class Meta:
        database = DB  # Specify Database
        table_name = 'devices'  # Specify table name

# Define Pydance model DeviceModel
class DeviceModel(BaseModel):
    id: Optional[int]  # Define the ID field
    user_id: str  # Define the user_id field as a string type
    device_id: str  # Define the Device_id field as a string type
    created_at: int  # Define the 'creatd_at' field as an integer type

# Define the DevicesTable class for manipulating the Devices table
class DevicesTable:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        self.db.create_tables([Device])  # Create Device Table

    # Insert new device
    def insert_new_device(self, user_id: str, device_id: str) -> Optional[DeviceModel]:
        log.info("insert_new_device")
=======
# 定义Device模型
class Device(Model):
    id = AutoField()  # 使用AutoField作为主键
    user_id = CharField()  # 用户ID
    device_id = CharField()  # 设备ID
    created_at = BigIntegerField(default=lambda: int(time.time()))  # 创建时间

    class Meta:
        database = DB  # 指定数据库
        table_name = 'devices'  # 指定表名

# 定义Pydantic模型DeviceModel
class DeviceModel(BaseModel):
    id: Optional[int]  # 定义id字段为可选
    user_id: str  # 定义user_id字段，类型为字符串
    device_id: str  # 定义device_id字段，类型为字符串
    created_at: int  # 定义created_at字段，类型为整数

# 定义DevicesTable类，用于操作Devices表
class DevicesTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([Device])  # 创建Device表

    # 插入新设备
    def insert_new_device(self, user_id: str, device_id: str) -> Optional[DeviceModel]:
        log.info("insert_new_device插入新设备")
>>>>>>> fingerprintAuth-out

        device_data = {
            "user_id": user_id,
            "device_id": device_id,
            "created_at": int(time.time())
        }
<<<<<<< HEAD
        result = Device.create(**device_data)  # Create a new device in the database
        if result:
            return DeviceModel(id=result.id, **device_data)  # Return the created device
        else:
            return None  # If the creation fails, return None

    # Retrieve the device based on the device ID
    def get_device_by_id(self, device_id: str) -> Optional[DeviceModel]:
        try:
            device = Device.get(Device.device_id == device_id)  # Retrieve devices from the database
            return DeviceModel(**model_to_dict(device))  # Convert database objects to Pydantic models and return
        except Device.DoesNotExist:
            return None  # If the query fails, return None

    # Update device information
    def update_device_by_id(self, device_id: str, updated: dict) -> Optional[DeviceModel]:
        try:
            query = Device.update(**updated).where(Device.device_id == device_id)  # Update device information
            query.execute()  # Perform update operation
            device = Device.get(Device.device_id == device_id)  # Search for updated devices
            return DeviceModel(**model_to_dict(device))  # Convert database objects to Pydantic models and return
        except Device.DoesNotExist:
            return None  # If the update fails, return None

    # Delete device information
    def delete_device_by_id(self, device_id: str) -> bool:
        try:
            query = Device.delete().where(Device.device_id == device_id)  # Delete device records
            result = query.execute()  # Perform deletion operation
            return result > 0  # If the deletion is successful, return True; otherwise, return False
        except:
            return False  # If an exception occurs, return False

# Instantiate the DevicesTable class
=======
        result = Device.create(**device_data)  # 在数据库中创建新设备
        if result:
            return DeviceModel(id=result.id, **device_data)  # 返回创建的设备
        else:
            return None  # 如果创建失败，返回None

    # 根据device_id获取设备
    def get_device_by_id(self, device_id: str) -> Optional[DeviceModel]:
        try:
            device = Device.get(Device.device_id == device_id)  # 查询数据库中的设备
            return DeviceModel(**model_to_dict(device))  # 将数据库对象转换为Pydantic模型并返回
        except Device.DoesNotExist:
            return None  # 如果查询失败，返回None

    # 更新设备信息
    def update_device_by_id(self, device_id: str, updated: dict) -> Optional[DeviceModel]:
        try:
            query = Device.update(**updated).where(Device.device_id == device_id)  # 更新设备信息
            query.execute()  # 执行更新操作
            device = Device.get(Device.device_id == device_id)  # 查询更新后的设备
            return DeviceModel(**model_to_dict(device))  # 将数据库对象转换为Pydantic模型并返回
        except Device.DoesNotExist:
            return None  # 如果更新失败，返回None

    # 删除设备信息
    def delete_device_by_id(self, device_id: str) -> bool:
        try:
            query = Device.delete().where(Device.device_id == device_id)  # 删除设备记录
            result = query.execute()  # 执行删除操作
            return result > 0  # 如果删除成功，返回True，否则返回False
        except:
            return False  # 如果出现异常，返回False

# 实例化DevicesTable类
>>>>>>> fingerprintAuth-out
devices_table = DevicesTable(DB)
