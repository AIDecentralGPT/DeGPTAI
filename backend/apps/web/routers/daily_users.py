from fastapi import APIRouter
from fastapi import Depends
from utils.utils import (get_current_user)
from apps.web.models.daily_users import DailyUsersInstance

router = APIRouter()

# 更新当天活跃用户数
@router.post("/line")
async def daily_active_users_line(user=Depends(get_current_user)):
  start_time = "2025-06-01"
  list = DailyUsersInstance.get_active_users_list(start_time)
  return list