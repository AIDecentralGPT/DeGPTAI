from peewee import *
from pydantic import BaseModel
from typing import List, Union, Optional
from apps.web.internal.db import DB, aspect_database_operations
<<<<<<< HEAD
from playhouse.shortcuts import model_to_dict
=======
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
>>>>>>> fingerprintAuth-out
from datetime import datetime, date
import time
import uuid


class Conversation(Model):
<<<<<<< HEAD
    id = CharField(primary_key=True, default=str(uuid.uuid4)) #Primary key
    user_id = CharField() # user id
    model = CharField() # Model name
    chat_time = DateField()  # session date
    chat_num = IntegerField() # Total number of sessions
    created_at = BigIntegerField() # Creation time
    updated_at = BigIntegerField() # Update time
=======
    id = CharField(primary_key=True, default=str(uuid.uuid4)) #主键
    user_id = CharField() # 用户ID
    model_type = CharField() # 模型类型
    chat_time = DateField()  # 会话日期
    chat_num = IntegerField() # 会话总数
    created_at = BigIntegerField() # 创建时间
    updated_at = BigIntegerField() # 更新时间
>>>>>>> fingerprintAuth-out

    class Meta:
        database = DB
        table_name = 'conversation'

class ConversationModel(BaseModel):
<<<<<<< HEAD
    id: str # Primary key
    user_id: str # user id
    model: str # Model name
    chat_time: datetime  # session date
    chat_num: int # Total number of sessions
    created_at: int # Creation time
    updated_at: int # Update time


class ConversationRequest(BaseModel):
    models: list


# Define the ConversationTable class for manipulating the ConversationTable
class ConversationTable:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        db.create_tables([Conversation])

    def insert(self, user_id: str, model: str) -> bool:
=======
    id: str # 主键
    user_id: str # 用户ID
    model_type: str # 模型类型
    chat_time: datetime  # 会话日期
    chat_num: int # 会话总数
    created_at: int # 创建时间
    updated_at: int # 更新时间


class ConversationRequest(BaseModel):
    model: str


# 定义ConversationTable类，用于操作Conversation表
class ConversationTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        db.create_tables([Conversation])

    def insert(self, user_id: str, model_type: str) -> bool:
>>>>>>> fingerprintAuth-out
      try:
        conversation = ConversationModel(
          id = str(uuid.uuid4()),
          user_id = user_id,
<<<<<<< HEAD
          model = model,
=======
          model_type = model_type,
>>>>>>> fingerprintAuth-out
          chat_time =  date.today(),
          chat_num = 1,
          created_at = int(time.time()),
          updated_at = int(time.time())
        )
        Conversation.create(**conversation.model_dump())
        return True
<<<<<<< HEAD
      except:
=======
      except Exception as e:
        print("========conversation insert========", e)
>>>>>>> fingerprintAuth-out
        return False

    def update(self, conversation: ConversationModel) -> bool:
      try:
        chat_num = conversation.chat_num + 1
        update = Conversation.update(chat_num=chat_num, updated_at=int(time.time())).where(Conversation.id==conversation.id)
        update.execute()
        return True
      except Exception as e:
        return False

<<<<<<< HEAD
    def get_info_by_userid_model_date(self, user_id: str, model: str, chat_time: date) -> Optional[ConversationModel]:
      try:
        conversation = Conversation.get_or_none(Conversation.user_id == user_id, Conversation.model == model, SQL('date(chat_time)') == chat_time)
        if conversation is None:
          return None
        else:
          conversation_dict = model_to_dict(conversation)  # Convert database objects to dictionaries
          conversation_model = ConversationModel(**conversation_dict)  # Convert dictionary to Pydantic model
          return conversation_model
      except Exception as e:
        print("========================", e)
        return None
      
    # Obtain the usage status of multiple models by users today
    def get_info_by_userid_models_date(self, user_id: str, models: list, chat_time: date) -> Optional[List[ConversationModel]]:
      try:
        conversations = Conversation.select().where(Conversation.user_id == user_id, Conversation.model.in_(models), SQL('date(chat_time)') == chat_time)
        # Convert database objects to dictionaries
        conversation_list = [ConversationModel(**model_to_dict(conversation)) for conversation in conversations]
        return conversation_list  
      except Exception as e:
        print("========================", e)
        return None

# Instantiate ConversationTable class
=======
    def get_info_by_userid_mtype_date(self, user_id: str, model_type: str, chat_time: date) -> Optional[ConversationModel]:
      try:
        conversation = Conversation.get_or_none(Conversation.user_id == user_id, Conversation.model_type == model_type, SQL('date(chat_time)') == chat_time)
        if conversation is None:
          return None
        else:
          conversation_dict = model_to_dict(conversation)  # 将数据库对象转换为字典
          conversation_model = ConversationModel(**conversation_dict)  # 将字典转换为Pydantic模型
          return conversation_model
      except Exception as e:
        print("=============get_info_by_userid_mtype_date===========", e)
        return None
      
    #获取用户今天多个模型使用情况
    def get_info_by_userid_mtypes_date(self, user_id: str, types: list, chat_time: date) -> Optional[List[ConversationModel]]:
      try:
        conversations = Conversation.select().where(Conversation.user_id == user_id, Conversation.model_type.in_(types), SQL('date(chat_time)') == chat_time)
        # 将数据库对象转换为字典
        conversation_list = [ConversationModel(**model_to_dict(conversation)) for conversation in conversations]
        return conversation_list  
      except Exception as e:
        print("===========get_info_by_userid_mtypes_date=============", e)
        return None

# 实例化ConversationTable类
>>>>>>> fingerprintAuth-out
ConversationInstance = ConversationTable(DB)

