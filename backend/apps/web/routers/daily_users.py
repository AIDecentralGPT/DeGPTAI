from fastapi import APIRouter
from fastapi import Depends
from utils.utils import (get_current_user)
from apps.web.models.daily_users import DailyUsersInstance
from datetime import datetime, timedelta

router = APIRouter()

# 获取每天活跃用户数列表
# @router.post("/line")
# async def daily_active_users_line(user=Depends(get_current_user)):
#   # start_time = "2025-06-01"
#   current_date = datetime.now().date()
#   # 计算15天前的日期
#   fifteen_days_ago = current_date - timedelta(days=14)
#   start_time = fifteen_days_ago.strftime("%Y-%m-%d")

#   list = DailyUsersInstance.get_active_users_list(start_time)
#   return list

# 获取近15天活跃用户数表格
@router.post("/line")
async def daily_active_users_line(user=Depends(get_current_user)):
  # start_time = "2025-06-01"
  current_date = datetime.now().date()
  # 计算15天前的日期
  fifteen_days_ago = current_date - timedelta(days=14)
  start_time = fifteen_days_ago.strftime("%Y-%m-%d")

  list = DailyUsersInstance.get_active_users_line(start_time)
  return list