from peewee import *
from pydantic import BaseModel
from apps.web.internal.db import DB, aspect_database_operations
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from datetime import date, datetime
import uuid
import pytz


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
      
      datelist = [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.65, 
                    0.76, 0.82, 0.865, 0.888, 0.99, 0.993, 0.996, 1, 1, 1, 1, 1, 1]
      gmt_minus_7 = pytz.timezone('Etc/GMT-7')
      current_hour = datetime.now(gmt_minus_7).hour
      dailyusers_list[0].user_num = int(dailyusers_list[0].user_num * datelist[current_hour])
      return dailyusers_list
    except Exception as e:
      return []
    
# 实例化DailyUsersTable类
DailyUsersInstance = DailyUsersTable(DB)