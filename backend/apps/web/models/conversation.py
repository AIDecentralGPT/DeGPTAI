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
    model_type = CharField() # 模型类型
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
    user_role: str # 用户角色
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

    def insert(self, user_id: str, user_role: str, model_type: str) -> bool:
      try:
        conversation = ConversationModel(
          id = str(uuid.uuid4()),
          user_id = user_id,
          user_role= user_role,
          model_type = model_type,
          chat_time =  date.today(),
          chat_num = 1,
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
        chat_num = conversation.chat_num + 1
        update = Conversation.update(chat_num=chat_num, user_role = conversation.user_role,updated_at=int(time.time())).where(Conversation.id==conversation.id)
        update.execute()
        return True
      except Exception as e:
        return False

    # 获取当天的聊天数据根据模型类型
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

    # 获取本月的聊天数据根据模型类型（VIP用户使用）
    def get_info_by_userid_mtype_month(self, user_id: str, model_type: str, chat_time: date) -> Optional[int]:
      try:
        year_month = chat_time.strftime("%Y-%m")
        conversations = Conversation.select().where(Conversation.user_id == user_id, Conversation.model_type == model_type, fn.TO_CHAR(Conversation.chat_time, 'YYYY-MM') == year_month)
        if len(conversations) > 0:
          total = 0
          conversaton_list = [ConversationModel(**conversation) for conversation in conversations]
          for conversation in conversaton_list:
            if conversation.user_role == "kyc":
              if conversation.chat_num > 10:
                total = total + conversation.chat_num - 10
            elif conversation.user_role == "wallet":
              if conversation.chat_num > 5:
                total = total + conversation.chat_num - 5
            else:
              if conversation.chat_num > 3:
                total = total + conversation.chat_num - 3    
          return total
        else:
          return 0;
      except Exception as e:
        print("=============get_info_by_userid_mtype_month===========", e)
        return 0
      
    #获取用户今天多个模型使用情况
    def get_info_by_userid_user_total(self, user: UserModel, vips: List[VIPStatusModelResp], chat_time: date):
      try:
        result_data = {
          "free_total": {"use": 0, "total": 0, "type": "base"},
          "month_total": [
            {"use": 0, "total": 1000, "type": "base", "show": False, "vip": "basic"},
            {"use": 0, "total": 100, "type": "adv", "show": False, "vip": "basic"},
            {"use": 0, "total": 10, "type": "top", "show": False, "vip": "basic"},
            {"use": 0, "total": 5000, "type": "base", "show": False, "vip": "standard"},
            {"use": 0, "total": 300, "type": "adv", "show": False, "vip": "standard"},
            {"use": 0, "total": 100, "type": "top", "show": False, "vip": "standard"},
            {"use": 0, "total": 10000, "type": "base", "show": False, "vip": "pro"},
            {"use": 0, "total": 5000, "type": "adv", "show": False, "vip": "pro"},
            {"use": 0, "total": 250, "type": "top", "show": False, "vip": "pro"}
          ]
        }

        #判断用户角色赋值免费总条数
        free_total = 0
        if user.id.startswith("0x"):
          free_total = 5
          if user.verified:
            free_total = 10
        else:
          free_total = 3
        result_data["free_total"]["total"] = free_total

        # 判断用户VIP情况设置显示隐藏
        for vipStatu in vips:
          vip_type = vipStatu.vip
          for vipitem in result_data["month_total"]:
            if vipitem["vip"] == vip_type:
              vipitem["show"] = True
        
        year_month = chat_time.strftime("%Y-%m")
        conversations = Conversation.select().where(Conversation.user_id == user.id, fn.TO_CHAR(Conversation.chat_time, 'YYYY-MM') == year_month).order_by(Conversation.chat_time.desc())
        print("conversations", conversations)
        # 将数据库对象转换为字典
        conversation_list = [ConversationModel(**model_to_dict(conversation)) for conversation in conversations]
        print("conversation_list", conversation_list)
        base_use_total = 0
        adv_use_total = 0
        top_use_total = 0
        for conversation in conversation_list:
          # 获取免费条数使用情况
          if conversation.chat_time.date() == chat_time and conversation.model_type == "base":
            result_data["free_total"]["use"] = min(conversation.chat_num, free_total)
          # 获取VIP使用条数情况
          if conversation.model_type == "base":
            free_allowance = 10 if conversation.user_role == "kyc" else 5 if conversation.user_role == "wallet" else 3
            if conversation.chat_num > free_allowance:
              base_use_total += conversation.chat_num - free_allowance
          elif conversation.model_type == "adv":
            adv_use_total += conversation.chat_num
          elif conversation.model_type == "top":
            top_use_total += conversation.chat_num

        # 计算模型汇总数据
        for modeltype in ['base', 'adv', 'top']:
          # 不通类型赋值计算总数
          dim_total = base_use_total if modeltype == "base" else adv_use_total if modeltype == "adv" else top_use_total

          # 循环判断使用总数
          for modelitem in result_data["month_total"]:
            if modelitem["type"] == modeltype:
              if dim_total > modelitem["total"]:
                modelitem["use"] = modelitem["total"]
                dim_total -= modelitem["total"]
              else:
                modelitem["use"] = dim_total
                dim_total = 0
        
        return result_data  
      except Exception as e:
        print("===========get_info_by_userid_user_total=============", e)
        return result_data

# 实例化ConversationTable类
ConversationInstance = ConversationTable(DB)

