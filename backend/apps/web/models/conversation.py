from peewee import *
from pydantic import BaseModel
from typing import List, Union, Optional
from apps.web.internal.db import DB, aspect_database_operations
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from datetime import datetime, date
import time
import uuid


class Conversation(Model):
    id = CharField(primary_key=True, default=str(uuid.uuid4)) #主键
    user_id = CharField() # 用户ID
    model = CharField() # 模型名称
    chat_time = DateField()  # 会话日期
    chat_num = IntegerField() # 会话总数
    created_at = BigIntegerField() # 创建时间
    updated_at = BigIntegerField() # 更新时间

    class Meta:
        database = DB
        table_name = 'conversation'

class ConversationModel(BaseModel):
    id: str # 主键
    user_id: str # 用户ID
    model: str # 模型名称
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

    def insert(self, user_id: str, model: str) -> bool:
      try:
        conversation = ConversationModel(
          id = str(uuid.uuid4()),
          user_id = user_id,
          model = model,
          chat_time =  date.today(),
          chat_num = 1,
          created_at = int(time.time()),
          updated_at = int(time.time())
        )
        Conversation.create(**conversation.model_dump())
        return True
      except:
        return False

    def update(self, conversation: ConversationModel) -> bool:
      try:
        chat_num = conversation.chat_num + 1
        update = Conversation.update(chat_num=chat_num, updated_at=int(time.time())).where(Conversation.id==conversation.id)
        update.execute()
        return True
      except Exception as e:
        return False

    def get_info_by_userid_model_date(self, user_id: str, model: str, chat_time: date) -> Optional[ConversationModel]:
      try:
        conversation = Conversation.get_or_none(Conversation.user_id == user_id, Conversation.model == model, SQL('date(chat_time)') == chat_time)
        if conversation is None:
          return None
        else:
          conversation_dict = model_to_dict(conversation)  # 将数据库对象转换为字典
          conversation_model = ConversationModel(**conversation_dict)  # 将字典转换为Pydantic模型
          return conversation_model
      except Exception as e:
        print("========================", e)
        return None

# 实例化ConversationTable类
ConversationInstance = ConversationTable(DB)

