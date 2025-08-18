from peewee import *
from pydantic import BaseModel
from apps.web.internal.db import DB, aspect_database_operations
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from datetime import date, datetime, timedelta
import uuid
import time

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
  def refresh_active_today(self, checktime: int):
    if self.is_same_day(checktime, int(time.time())) == False:
      # 获取当前日期
      active_time = date.today()
      try:
        dailyusers = DailyUsers.get_or_none(SQL('date(active_time)') == active_time)
        if dailyusers is None:
          dailyusers = DailyUsersModel(
            id = str(uuid.uuid4()),
            user_num =  1,
            active_time = active_time
          )
          DailyUsers.create(**dailyusers.model_dump())
        else:
          dailyuser_dict = model_to_dict(dailyusers)
          dailyuser_model = DailyUsersModel(**dailyuser_dict)
          user_num = dailyuser_model.user_num + 1
          update = DailyUsers.update(user_num = user_num).where(DailyUsers.id == dailyuser_model.id)
          update.execute()
      except Exception as e:
        print("=================", e)

  # check same datetime
  def is_same_day(self, timestamp1, timestamp2):
    # 将时间戳转换为datetime对象
    dt1 = datetime.fromtimestamp(timestamp1)
    dt2 = datetime.fromtimestamp(timestamp2)
    # 比较年、月、日是否都相同
    return (dt1.year == dt2.year and 
            dt1.month == dt2.month and 
            dt1.day == dt2.day)

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
      
      # datelist = [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.65, 
      #               0.76, 0.82, 0.865, 0.888, 0.99, 0.993, 0.996, 1, 1, 1, 1, 1, 1]
      # current_hour = datetime.now().hour
      # dailyusers_list[0].user_num = int(dailyusers_list[0].user_num * datelist[current_hour])
      return dailyusers_list
    except Exception as e:
      return []
    
  # 获取用户活跃数Line
  def get_active_users_line(self, start_time: str):
    try:
      dailyuserss = DailyUsers.select().where(DailyUsers.active_time >= start_time).order_by(DailyUsers.active_time.asc())
      dailyusers_list = [DailyUsersModel(**model_to_dict(dailyusers)) for dailyusers in dailyuserss]
      date_list = []
      users_list = []

      # 获取当前日期
      current_date = datetime.now().date()
      # 循环计算近15天的日期
      for i in range(14, -1, -1):
          # 计算第i天前的日期
          date = current_date - timedelta(days=i)
          # 转换为"月日"格式（例如：08-12）
          month_day = date.strftime("%m-%d")
          date_list.append(month_day)

          user_num = next((item.user_num for item in dailyusers_list if item.active_time.strftime("%m-%d") == month_day), 0)
          users_list.append(user_num)

      return {
        "date_list": date_list,
        "users_list": users_list
      }
    except Exception as e:
      print("===============", e)
      return {
        "date_list": [],
        "users_list": []
      }
    
# 实例化DailyUsersTable类
DailyUsersInstance = DailyUsersTable(DB)