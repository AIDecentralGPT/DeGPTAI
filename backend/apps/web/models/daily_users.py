from peewee import *
from pydantic import BaseModel
from apps.web.internal.db import DB, aspect_database_operations
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from datetime import date
import uuid


class DailyUsers(Model):
  id = CharField(primary_key=True, default=str(uuid.uuid4)) #主键
  user_num = IntegerField() # 用户数量
  active_time = DateField()  # 活跃日期

  class Meta:
    database = DB
    table_name = 'daily_users'

class DailyUsersModel(BaseModel):
  id: str # 主键
  user_num: int # 用户数量
  active_time: date  # 活跃日期

class DailyUsersTable:
  def __init__(self, db):
    self.db = db  # 初始化数据库实例
    db.create_tables([DailyUsers])

  # 获取今日用户活跃数
  def today_active_users(self):
    # 获取当前日期
    active_time = date.today()
    try:
      dailyusers = DailyUsers.get_or_none(SQL('date(active_time)') == active_time)
      if dailyusers is None:
        return 0
      else:
        dailyuser_dict = model_to_dict(dailyusers)  # 将数据库对象转换为字典
        dailyuser_model = DailyUsersModel(**dailyuser_dict)  # 将字典转换为Pydantic模型
        return dailyuser_model.user_num
    except:
      return 0
  
  # 获取用户活跃数列表
  def get_active_users_list(self, start_time: str):
    try:
      dailyuserss = DailyUsers.select().where(DailyUsers.active_time >= start_time).order_by(DailyUsers.active_time.desc())
      dailyusers_list = [DailyUsersModel(**model_to_dict(dailyusers)) for dailyusers in dailyuserss]
      return dailyusers_list
    except Exception as e:
      return []
    
# 实例化DailyUsersTable类
DailyUsersInstance = DailyUsersTable(DB)