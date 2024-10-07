from fastapi import APIRouter, Depends, HTTPException, Request
from apps.web.models.users import User
from apps.web.models.device import Device
from apps.web.models.ip_log import IpLog
from apps.web.models.rewards import RewardsTableInstance, RewardsRequest
from utils.utils import get_verified_user
from playhouse.shortcuts import model_to_dict
import time
from datetime import date

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

    success = RewardsTableInstance.send_reward(user_id, 200)
    if success:
        return {"message": "Reward sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send reward")



    # # 校验设备ID
    # device_valid = await check_device(user_id, device_id)
    # if not device_valid:
    #     raise HTTPException(status_code=400, detail="Device already registered for this user.")

    # # 校验IP地址
    # client_ip = request.client.host
    # ip_valid = await check_ip(user_id, client_ip)
    # if not ip_valid:
    #     raise HTTPException(status_code=400, detail="IP address already used for rewards.")

    # 处理奖励领取逻辑
    # 这里只是一个示例，你需要根据你的具体业务逻辑来实现
    return {"message": "Reward claimed successfully."}


# 用户签到
@router.post("/clock_in")
async def clock_in(request: Request, user=Depends(get_verified_user)):
    # 获取今天的日期
    today = date.today()
    # 发送奖励
    reward_type = "clock_in"  # 例如每日签到奖励
    # 检查用户是否已经在今天获得过奖励
    existing_rewards = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id, today, reward_type)
    print("existing_rewards:", existing_rewards)
    if existing_rewards:
        raise HTTPException(status_code=400, detail="You have received 500 DGC points，you can convert your points into cash")
    
    success = RewardsTableInstance.create_reward(user.id, 10, reward_type)
    if success:
        return {"ok": True, "message": "You have received 500 DGC points !"}
    else:
        raise HTTPException(status_code=500, detail="Failed to received reward")

# 用户签到确认
@router.post("/clock_in_check")
async def clock_in_check(request: RewardsRequest, user=Depends(get_verified_user)):
    # 获取签到记录
    rewards_history= RewardsTableInstance.get_rewards_by_id(request.id, user.id)
    if rewards_history is None:
        raise HTTPException(status_code=400, detail="You Rewards History not found")
    
    result = RewardsTableInstance.send_reward(rewards_history.id, rewards_history.user_id, rewards_history.reward_amount, rewards_history.reward_type)
    if result is not None:
        return {"ok": True, "data": result}
    else:
        raise HTTPException(status_code=500, detail="Failed to received reward")
    
@router.get("/reward_count")
async def get_reward_count(user=Depends(get_verified_user)):
    today = date.today()
    
    # 查询 clock_in 类型奖励的次数
    clock_in_count = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id, today, "clock_in")
    
    # 查询 invite 类型奖励的次数
    invite_count = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id,  today,"invite")

    new_wallet = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id, today, "new_wallet")
    
    return {
        "clock_in": clock_in_count,
        "invite": invite_count,
        "new_wallet": new_wallet
    }

@router.get("/reward_history")
async def get_reward_count(user=Depends(get_verified_user)):
    
    # 查询 clock_in 类型奖励的次数
    rewards_history = RewardsTableInstance.get_rewards_by_user_id(user.id)

    return rewards_history
