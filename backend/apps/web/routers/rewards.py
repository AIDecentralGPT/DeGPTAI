from fastapi import APIRouter, Depends, HTTPException, Request
from apps.web.models.users import User
from apps.web.models.device import Device
from apps.web.models.ip_log import IpLog
from utils.utils import get_verified_user
from playhouse.shortcuts import model_to_dict
import time

router = APIRouter()

# 校验设备ID
async def check_device(user_id: str, device_id: str):
    try:
        user = User.get(User.id == user_id)
        existing_device = Device.get(Device.user == user, Device.device_id == device_id)
        return False  # 设备已经注册
    except Device.DoesNotExist:
        Device.create(user=user, device_id=device_id)
        return True  # 设备未注册，已添加

# 校验IP地址
async def check_ip(user_id: str, ip_address: str):
    try:
        existing_ip_log = IpLog.get(IpLog.ip_address == ip_address)
        return False  # IP地址已经使用过
    except IpLog.DoesNotExist:
        user = User.get(User.id == user_id)
        IpLog.create(user=user, ip_address=ip_address)
        return True  # IP地址未使用过，已添加

# 用户领取奖励
@router.post("/rewards/{user_id}/claim")
async def claim_reward(request: Request, user_id: str, device_id: str, user=Depends(get_verified_user)):
    # 校验设备ID
    device_valid = await check_device(user_id, device_id)
    if not device_valid:
        raise HTTPException(status_code=400, detail="Device already registered for this user.")

    # 校验IP地址
    client_ip = request.client.host
    ip_valid = await check_ip(user_id, client_ip)
    if not ip_valid:
        raise HTTPException(status_code=400, detail="IP address already used for rewards.")

    # 处理奖励领取逻辑
    # 这里只是一个示例，你需要根据你的具体业务逻辑来实现
    return {"message": "Reward claimed successfully."}
