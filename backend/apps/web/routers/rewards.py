from fastapi import APIRouter, Depends, HTTPException, Request
from apps.web.models.users import User, Users
from apps.web.models.device import Device
from apps.web.models.ip_log import IpLog
from apps.web.models.rewards import RewardsTableInstance, RewardsRequest, RewardsPageRequest, Rewards
from apps.web.api.rewardapi import RewardApiInstance
from utils.utils import get_verified_user
from datetime import date
import threading
import concurrent.futures

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

# 用户创建领取奖励
user_locks_dict = {}
@router.post("/creat_wallet_check")
async def creat_wallet_check(request: RewardsRequest, user=Depends(get_verified_user)):
    global user_locks_dict
    # 若用户对应的锁不存在，则创建并添加到字典
    user_key = user.id + "-new_waller"
    if user_key not in user_locks_dict:
        user_locks_dict[user.id + "-new_waller"] = threading.Lock()
    user_lock = user_locks_dict[user.id + "-new_waller"]
    # 获取锁，若锁已被该用户其他线程占用，则等待
    user_lock.acquire()
    try:
        # 获取签到记录
        rewards_history= RewardsTableInstance.get_rewards_by_id(request.id)
        if rewards_history is None:
            raise HTTPException(status_code=400, detail="You Rewards History not found")
        
        # 是否已领取校验
        if rewards_history.status:
            return {"ok": True, "data": rewards_history}
        
        # 校验用户是否已经完成kyc认证
        user_find = Users.get_user_by_id(user.id)
        if not user_find.verified:
            raise HTTPException(status_code=500, detail="Please complete the KYC verification !")
        
        # 判断领取那种奖励
        if rewards_history.invitee is not None:
            # 赋值奖励信息
            inviteReward = None;
            inviteeReward = None;
            rewards = RewardsTableInstance.get_rewards_by_invitee(rewards_history.invitee)
            if len(rewards) != 2:
                raise HTTPException(status_code=500, detail="Failed to received reward")       
            for reward in rewards:
                if reward.reward_type == 'invite':
                    if reward.show:
                        inviteReward = reward
                else:
                    inviteeReward = reward
            # 领取邀请奖励
            result = RewardApiInstance.inviteRewardThread(inviteReward, inviteeReward)
            if result is not None:
                return {"ok": True, "data": result}
            else:
                raise HTTPException(status_code=500, detail="Failed to received reward")
        else:
            # 领取注册奖励
            result = RewardApiInstance.registReward(rewards_history.id, rewards_history.user_id)
            if result is not None:
                return {"ok": True, "data": result}
            else:
                raise HTTPException(status_code=500, detail="Failed to received reward")
            
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Failed to received reward")
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        user_lock.release()

# 用户签到
@router.post("/clock_in")
async def clock_in(user=Depends(get_verified_user)):
    # 获取今天的日期
    today = date.today()
    # 发送奖励
    reward_type = "clock_in"  # 例如每日签到奖励
    # 检查用户是否已经在今天获得过奖励
    existing_rewards = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id, today, reward_type)
    print("existing_rewards:", existing_rewards)
    if existing_rewards:
        raise HTTPException(status_code=400, detail="You have received 100 DGC points !")
    
    rewards = RewardsTableInstance.create_reward(user.id, 100, reward_type)
    if rewards is not None:
        # 校验用户是否已经kyc
        if user.verified:
            # 领取奖励
            RewardApiInstance.dailyReward(rewards.id, user.id)
        return {"ok": True, "message": "You have received 100 DGC points !"}
    else:
        raise HTTPException(status_code=500, detail="Failed to received reward")

# 用户签到领取奖励
@router.post("/clock_in_check")
async def clock_in_check(request: RewardsRequest, user=Depends(get_verified_user)):

    global user_locks_dict
    # 若用户对应的锁不存在，则创建并添加到字典
    user_key = user.id + "-clock_in"
    if user_key not in user_locks_dict:
        user_locks_dict[user.id + "-clock_in"] = threading.Lock()
    user_lock = user_locks_dict[user.id + "-clock_in"]
    # 获取锁，若锁已被该用户其他线程占用，则等待
    user_lock.acquire()
    try:
        # 校验用户是否已经完成kyc认证
        user_find = Users.get_user_by_id(user.id)
        if not user_find.verified:
            raise HTTPException(status_code=500, detail="Please complete the KYC verification !")
        
        # 获取签到记录
        rewards_history= RewardsTableInstance.get_rewards_by_id(request.id)
        if rewards_history is None:
            raise HTTPException(status_code=400, detail="You Rewards History not found")
        
        # 是否已领取校验
        if rewards_history.status:
            return {"ok": True, "data": rewards_history}
        
        # 领取奖励
        result = RewardApiInstance.dailyReward(rewards_history.id, user.id)
        if result is not None:
            return {"ok": True, "data": result}
        else:
            raise HTTPException(status_code=500, detail="Clockin rewards can only be obtained once within a 24-hour period，you can try later.")
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Failed to received reward")
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        user_lock.release()
    
# 用户邀请领取奖励
@router.post("/invite_check")
async def invite_check(request: RewardsRequest, user=Depends(get_verified_user)):
    # 获取签到记录
    rewards_history= RewardsTableInstance.get_rewards_by_id(request.id)
    if rewards_history is None:
        raise HTTPException(status_code=400, detail="You Rewards History not found")

    if rewards_history.reward_type == 'invite':
        if rewards_history.status:
            return {"ok": True, "data": rewards_history}
        else:
            rewards = RewardsTableInstance.get_rewards_by_invitee(rewards_history.invitee)
            inviteReward = None;
            inviteeReward = None;
            if len(rewards) != 2:
                raise HTTPException(status_code=500, detail="Failed to received reward")       
            for reward in rewards:
                if reward.reward_type == 'invite':
                    if reward.show:
                        inviteReward = reward
                else:
                    inviteeReward = reward
            if inviteeReward.status:
                inviteResult = RewardApiInstance.inviteReward(inviteReward, inviteeReward)
                return {"ok": True, "data": inviteResult}
            else:
                raise HTTPException(status_code=400, detail="Your friend not complete the KYC verification.") 
    else: 
        raise HTTPException(status_code=400, detail="Your friend not complete the KYC verification.")     
    
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

@router.post("/reward_history")
async def get_reward_count(request: RewardsPageRequest,user=Depends(get_verified_user)):
    
    print("=============page=============", request);
    # 查询 clock_in 类型奖励的次数
    rewards_history = RewardsTableInstance.get_rewards_by_user_id(user.id, request.pageNum, request.pageSize)
    total = RewardsTableInstance.get_rewards_count_by_user_id(user.id);

    return {
        "row" :rewards_history,
        "total": total
    }

@router.post("/invite_total")
async def get_invite_total(user=Depends(get_verified_user)):
    if user is not None:
        invite_total = RewardsTableInstance.get_invitee_total()
        invite_reward_total = RewardsTableInstance.get_invitee_reward_total()
        invite_issue_total = RewardsTableInstance.get_issue_invitee_reward_total()
        return {
            "invite_total": invite_total,
            "invite_reward_total": invite_reward_total,
            "invite_issue_total": invite_issue_total
        }

register_rewards_locks_dict = {}
@router.post("/sync_regist_rewards")
async def sync_regist_rewards(user=Depends(get_verified_user)):
    global register_rewards_locks_dict
    # 若用户对应的锁不存在，则创建并添加到字典
    register_rewards_lock =  "system-async-register-rewards"
    if register_rewards_lock not in register_rewards_locks_dict:
        register_rewards_locks_dict[register_rewards_lock] = threading.Lock()
    register_rewards_lock = register_rewards_locks_dict[register_rewards_lock]
    register_rewards_lock.acquire()
    try:
        if user is not None:
            rewards = RewardsTableInstance.sync_regist_rewards()
            with concurrent.futures.ThreadPoolExecutor(max_workers = 20) as executor:
                results = executor.map(send_regist_reward, rewards)
            return {"ok": True, "message": "Success"}
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Failed to received reward")
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        print("====================register_rewards_lock.release==================")
        register_rewards_lock.release()

def send_regist_reward(reward: Rewards):
    RewardApiInstance.inviteReward

@router.get("/dbc_rate")
async def get_dbc_rate(user=Depends(get_verified_user)): 
    # 查询dbc汇率 默认0.00198537(第一次查询的值)
    try:
        dbc_rate = RewardApiInstance.getDbcRate()
        if dbc_rate is not None:
            return dbc_rate
        else:
            return 0.0002
    except Exception as e:
        return 0.0002
