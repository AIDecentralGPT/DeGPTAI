from peewee import *
from pydantic import BaseModel
from typing import List, Union, Optional
from apps.web.internal.db import DB, aspect_database_operations
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from datetime import datetime, date
import time
import uuid

from apps.web.models.vipstatus import VIPStatusModelResp
from apps.web.models.users import UserModel


class Conversation(Model):
    id = CharField(primary_key=True, default=str(uuid.uuid4)) #主键
    user_id = CharField() # 用户ID
    user_role = CharField() # 用户角色
    equip_id = CharField() # 设备ID
    model_type = CharField() # 模型类型
    chat_time = DateField()  # 会话日期
    chat_num = IntegerField() # 会话总数
    vip = CharField() # 消耗次数所诉VIP
    created_at = BigIntegerField() # 创建时间
    updated_at = BigIntegerField() # 更新时间

    class Meta:
        database = DB
        table_name = 'conversation'

class ConversationModel(BaseModel):
    id: str # 主键
    user_id: str # 用户ID
    user_role: str # 用户角色
    equip_id: Optional[str]= None # 设备ID
    model_type: str # 模型类型
    chat_time: date  # 会话日期
    chat_num: int # 会话总数
    vip: Optional[str]= None # 消耗次数所诉VIP
    created_at: int # 创建时间
    updated_at: int # 更新时间


class ConversationRequest(BaseModel):
    model: str
    equip_id: str


# 定义ConversationTable类，用于操作Conversation表
class ConversationTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        db.create_tables([Conversation])

    def insert(self, user_id: str, user_role: str, equip_id: str, model_type: str, vip: str, chat_num: int) -> bool:
      try:
        conversation = ConversationModel(
          id = str(uuid.uuid4()),
          user_id = user_id,
          user_role= user_role,
          equip_id = equip_id,
          model_type = model_type,
          chat_time =  date.today(),
          chat_num = chat_num,
          vip = vip,
          created_at = int(time.time()),
          updated_at = int(time.time())
        )
        Conversation.create(**conversation.model_dump())
        return True
      except Exception as e:
        print("========conversation insert========", e)
        return False

    def update(self, conversation: ConversationModel) -> bool:
      try:
        chat_num = conversation.chat_num
        update = Conversation.update(chat_num=chat_num, user_role = conversation.user_role,updated_at=int(time.time())).where(Conversation.id==conversation.id)
        update.execute()
        return True
      except Exception as e:
        return False

    # 获取非会员用户当天的聊天数据
    def get_info_by_user_mtype_date(self, user_id: str, user_role: str, model_type: str, chat_time: date) -> Optional[ConversationModel]:
      try:
        conversation = Conversation.get_or_none(Conversation.user_id == user_id, Conversation.user_role == user_role, Conversation.model_type == model_type, 
                            SQL('date(chat_time)') == chat_time, Conversation.vip.is_null(True))
        if conversation is None:
          return None
        else:
          conversation_dict = model_to_dict(conversation)  # 将数据库对象转换为字典
          conversation_model = ConversationModel(**conversation_dict)  # 将字典转换为Pydantic模型
          return conversation_model
      except Exception as e:
        print("=============get_info_by_userid_mtype_date===========", e)
        return None
      
    # 获会员用户当天的聊天数据
    def get_info_by_user_mtype_vip_date(self, user_id: str, user_role: str, model_type: str, vip: str, chat_time: date) -> Optional[ConversationModel]:
      try:
        conversation = Conversation.get_or_none(Conversation.user_id == user_id, Conversation.user_role == user_role, Conversation.model_type == model_type, 
                            SQL('date(chat_time)') == chat_time, Conversation.vip==vip)
        if conversation is None:
          return None
        else:
          conversation_dict = model_to_dict(conversation)  # 将数据库对象转换为字典
          conversation_model = ConversationModel(**conversation_dict)  # 将字典转换为Pydantic模型
          return conversation_model
      except Exception as e:
        print("=============get_info_by_userid_mtype_date===========", e)
        return None
      
    # 获取会员某个时间段内用户会话总数 
    def get_info_by_userid_mtype_between(self, user_id: str, model_type: str, start_time: date) -> Optional[int]:
      try:
        conversations = Conversation.select().where(
            Conversation.user_id == user_id,
            Conversation.model_type == model_type,
            Conversation.chat_time >= start_time,
            Conversation.vip.is_null(False)
        )
        return sum(conv.chat_num for conv in conversations)
      except Exception as e:
        return 0

    # 获取同一设备非vip的钱包用户聊天总数最大的一条数据
    def get_info_by_equipid(self, equip_id: str, user_role: str, model_type: str, chat_time: date) -> Optional[ConversationModel]:
      try:
        conversation = Conversation.filter(Conversation.equip_id == equip_id,Conversation.user_role == user_role, Conversation.model_type == model_type,
            SQL('date(chat_time)') == chat_time, Conversation.vip.is_null(True)).order_by(Conversation.chat_num.desc()).first()
        if conversation is None:
          return None
        else:
          conversation_dict = model_to_dict(conversation)  # 将数据库对象转换为字典
          conversation_model = ConversationModel(**conversation_dict)  # 将字典转换为Pydantic模型
          return conversation_model
      except Exception as e:
        print("=============get_info_by_equipid===========", e)
        return None
      
    #获取用户今天多个模型使用情况
    def get_info_by_userid_user_total(self, user: UserModel, vips: List[VIPStatusModelResp], chat_time: date):
      try:
        result_data = {
          "free_total": {"use": 0, "total": 0, "type": "base", "show": False},
          "month_total": [
            {"use": 0, "total": 1000, "type": "base", "show": False, "vip": "basic", "time": "month"},
            {"use": 0, "total": 100, "type": "adv", "show": False, "vip": "basic", "time": "month"},
            {"use": 0, "total": 10, "type": "top", "show": False, "vip": "basic", "time": "month"},
            {"use": 0, "total": 5000, "type": "base", "show": False, "vip": "standard", "time": "month"},
            {"use": 0, "total": 300, "type": "adv", "show": False, "vip": "standard", "time": "month"},
            {"use": 0, "total": 100, "type": "top", "show": False, "vip": "standard", "time": "month"},
            {"use": 0, "total": 10000, "type": "base", "show": False, "vip": "pro", "time": "month"},
            {"use": 0, "total": 5000, "type": "adv", "show": False, "vip": "pro", "time": "month"},
            {"use": 0, "total": 250, "type": "top", "show": False, "vip": "pro", "time": "month"}
          ]
        }

        #VIP会员显示
        if len(vips) > 0:
          min_start_date = min(vips, key=lambda x: x.start_date).start_date
          conversations = Conversation.select().where(Conversation.user_id == user.id, Conversation.chat_time >= min_start_date).order_by(Conversation.chat_time.desc())
          conversation_list = [ConversationModel(**model_to_dict(conversation)) for conversation in conversations]
          #获取所有聊天记录
          for vipStatu in vips:
            for vipitem in result_data["month_total"]:
              if vipitem["vip"] == vipStatu.vip:
                vipitem["show"] = True
                vipitem["time"] = vipStatu.type
                if len(conversation_list) > 0:
                  vip_conversations = [conv for conv in conversation_list if conv.vip == vipStatu.vip]
                  date_conversations = [conv for conv in vip_conversations if  vipStatu.start_date <= conv.chat_time <= vipStatu.end_date]
                  mtype_conversations = [conv for conv in date_conversations if  conv.model_type == vipitem["type"]]
                  vipitem["use"] = sum(conv.chat_num for conv in mtype_conversations) if mtype_conversations else 0
                else:
                  vipitem["use"] = 0
        # 非VIP会员显示
        else:
          free_total = 0
          userrole = "user"
          if user.id.startswith("0x"):
            free_total = 5
            userrole = "wallet"
            if user.verified:
              free_total = 10
              userrole = "kyc"
          else:
            free_total = 3
          result_data["free_total"]["total"] = free_total
          result_data["free_total"]["show"] = True
          freeconversation = self.get_info_by_user_mtype_date(user.id, userrole, "base", chat_time)
          result_data["free_total"]["use"] = 0 if freeconversation is None else freeconversation.chat_num

        return result_data  
      except Exception as e:
        print("===========get_info_by_userid_user_total=============", e)
        return result_data

# 实例化ConversationTable类
ConversationInstance = ConversationTable(DB)

