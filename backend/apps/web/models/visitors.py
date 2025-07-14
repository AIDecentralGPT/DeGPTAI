<<<<<<< HEAD
from peewee import Model, CharField
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import List, Union, Optional
from playhouse.shortcuts import model_to_dict
from utils.misc import get_gravatar_url
import uuid

# Define the Visitors model
class Visitors(Model):
    id = CharField(unique=True)  # Define a unique character field ID
    visitor_id = CharField()  # Define the character field visitor_id

    class Meta:
        database = DB  # Specify Database
        table_name = 'visitors'  # Specify table name

# Define Pydantic Model VisitorModel
class VisitorModel(BaseModel):
    id: str  # Define the ID field as a string type
    visitor_id: str  # Define the visitor_id field as a string type

# Define the VisitorsTable class for manipulating the VisitorsTable table
class VisitorsTable:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        self.db.create_tables([Visitors])  # Create Visitors table

    # Insert new visitor
    def insert_new_visitor(self, id: str, visitor_id: str) -> Optional[VisitorModel]:
        visitor = VisitorModel(id=id, visitor_id=visitor_id)  # Create VisitorModel instance
        result = Visitors.create(**visitor.dict())  # Create a new visitor in the database
        print("result: ", result,id, visitor_id)
        if result:
            return visitor  # Return the created visitor
        else:
            return None  # If the creation fails, return None

    # Retrieve visitors based on visitor_id
    def get_visitor_by_id(self, visitor_id: str) -> Optional[VisitorModel]:
        try:
            visitor = Visitors.get(Visitors.visitor_id == visitor_id)  # Query visitors in the database
            return VisitorModel(**model_to_dict(visitor))  # Convert database objects to Pydantic models and return
        except Visitors.DoesNotExist:
            return None  # If the query fails, return None

    # Update visitor information
    def update_visitor_by_id(self, visitor_id: str, updated: dict) -> Optional[VisitorModel]:
        try:
            query = Visitors.update(**updated).where(Visitors.visitor_id == visitor_id)
            query.execute()
            visitor = Visitors.get(Visitors.visitor_id == visitor_id)  # Query updated visitors
            return VisitorModel(**model_to_dict(visitor))  # Convert database objects to Pydantic models and return
        except Visitors.DoesNotExist:
            # If the update fails, return None
            return None

    # Delete visitor information
    def delete_visitor_by_id(self, visitor_id: str) -> bool:
        try:
            query = Visitors.delete().where(Visitors.visitor_id == visitor_id)
            result = query.execute()
            return result > 0  # If the deletion is successful, return True; otherwise, return False
        except:
            return False  # If an exception occurs, return False

# Instantiate VisitorsTable class
=======
from peewee import Model, CharField  # 导入Peewee中的Model和CharField
from apps.web.internal.db import DB  # 导入数据库实例DB
from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from typing import List, Union, Optional  # 导入类型提示
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from utils.misc import get_gravatar_url  # 导入获取Gravatar URL的方法
import uuid

# 定义Visitors模型
class Visitors(Model):
    id = CharField(unique=True)  # 定义唯一的字符字段id
    visitor_id = CharField()  # 定义字符字段visitor_id

    class Meta:
        database = DB  # 指定数据库
        table_name = 'visitors'  # 指定表名

# 定义Pydantic模型VisitorModel
class VisitorModel(BaseModel):
    id: str  # 定义id字段，类型为字符串
    visitor_id: str  # 定义visitor_id字段，类型为字符串

# 定义VisitorsTable类，用于操作Visitors表
class VisitorsTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([Visitors])  # 创建Visitors表

    # 插入新访客
    def insert_new_visitor(self, id: str, visitor_id: str) -> Optional[VisitorModel]:
        visitor = VisitorModel(id=id, visitor_id=visitor_id)  # 创建VisitorModel实例
        result = Visitors.create(**visitor.dict())  # 在数据库中创建新访客
        print("result: ", result,id, visitor_id)
        if result:
            return visitor  # 返回创建的访客
        else:
            return None  # 如果创建失败，返回None

    # 根据visitor_id获取访客
    def get_visitor_by_id(self, visitor_id: str) -> Optional[VisitorModel]:
        try:
            visitor = Visitors.get(Visitors.visitor_id == visitor_id)  # 查询数据库中的访客
            return VisitorModel(**model_to_dict(visitor))  # 将数据库对象转换为Pydantic模型并返回
        except Visitors.DoesNotExist:
            return None  # 如果查询失败，返回None

    # 更新访客信息
    def update_visitor_by_id(self, visitor_id: str, updated: dict) -> Optional[VisitorModel]:
        try:
            query = Visitors.update(**updated).where(Visitors.visitor_id == visitor_id)  # 更新访客信息
            query.execute()  # 执行更新操作
            visitor = Visitors.get(Visitors.visitor_id == visitor_id)  # 查询更新后的访客
            return VisitorModel(**model_to_dict(visitor))  # 将数据库对象转换为Pydantic模型并返回
        except Visitors.DoesNotExist:
            return None  # 如果更新失败，返回None

    # 删除访客信息
    def delete_visitor_by_id(self, visitor_id: str) -> bool:
        try:
            query = Visitors.delete().where(Visitors.visitor_id == visitor_id)  # 删除访客记录
            result = query.execute()  # 执行删除操作
            return result > 0  # 如果删除成功，返回True，否则返回False
        except:
            return False  # 如果出现异常，返回False

# 实例化VisitorsTable类
>>>>>>> fingerprintAuth-out
visitors_table = VisitorsTable(DB)
