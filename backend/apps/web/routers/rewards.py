from fastapi import APIRouter, Depends, HTTPException, Request
from apps.web.models.users import User, Users
from apps.web.models.device import Device
from apps.web.models.ip_log import IpLog
from apps.web.models.rewards import RewardsTableInstance, RewardsRequest, RewardsPageRequest, Rewards
from apps.web.api.rewardapi import RewardApiInstance
from apps.web.models.reward_data import RewardDateTableInstance
from utils.utils import get_verified_user
from datetime import date, datetime
import threading
import concurrent.futures
from apps.web.api.rewardapi import ClockInAmount

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

# 用户创建领取奖励
user_locks_dict = {}
@router.post("/creat_wallet_check")
async def creat_wallet_check(request: RewardsRequest, user=Depends(get_verified_user)):
    global user_locks_dict
    # 若用户对应的锁不存在，则创建并添加到字典
    if user.id not in user_locks_dict:
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
        
        # 领取注册奖励
        rewards_history = RewardApiInstance.registReward(rewards_history.id, rewards_history.user_id)

        return {"ok": True, "data": rewards_history}
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Failed to received reward")
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        user_lock.release()

# 用户签到
@router.post("/clock_in")
async def clock_in(user=Depends(get_verified_user)):
    if not user.verified:
        raise HTTPException(status_code=500, detail="Please complete the KYC verification !")
    # 获取今天的日期
    today = date.today()
    # 判断是否kyc认证超过180天
    if user.face_time is not None:
        face_date = user.face_time.date()
        days_diff = (today - face_date).days
        if days_diff > 180:
            raise HTTPException(status_code=500, detail="The check-in reward has expired!")
    else:
        raise HTTPException(status_code=500, detail="The check-in reward has expired!")

    rewarddate = RewardDateTableInstance.get_current_open()
    if rewarddate is not None:
        current_date = datetime.now().date()
        if current_date < rewarddate.start_time.date() or current_date > rewarddate.end_time.date():
            raise HTTPException(status_code=400, detail="The reward program has ended !")
    else:
       raise HTTPException(status_code=400, detail="The reward program has ended !") 
    # 发送奖励
    reward_type = "clock_in"  # 例如每日签到奖励
    # 检查用户是否已经在今天获得过奖励
    existing_rewards = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id, today, reward_type)
    if existing_rewards:
        raise HTTPException(status_code=400, detail="You have received {{clockin}} DGC points !")
    
    rewards = RewardsTableInstance.create_reward(user.id, ClockInAmount, reward_type)
    if rewards is not None:
        # 领取奖励
        RewardApiInstance.dailyReward(rewards.id, user.id)
        # 判断是否发放邀请奖励
        checkInviteReward(user.id)
            
        return {"ok": True, "message": "You have received {{clockin}} DGC points !"}
    else:
        raise HTTPException(status_code=500, detail="Failed to received reward")

# 用户签到领取奖励
@router.post("/clock_in_check")
async def clock_in_check(request: RewardsRequest, user=Depends(get_verified_user)):

    global user_locks_dict
    # 若用户对应的锁不存在，则创建并添加到字典
    if user.id not in user_locks_dict:
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
        
        # 校验奖励时间是否过期
        if rewards_history.reward_date.date() != date.today():
            raise HTTPException(status_code=400, detail="You Rewards History has expired")
        
        # 是否已领取校验
        if rewards_history.status:
            return {"ok": True, "data": rewards_history}
        
        # 领取奖励
        result = RewardApiInstance.dailyReward(rewards_history.id, user.id)
        if result is not None:
            # 判断是否发放邀请奖励
            checkInviteReward(user.id)
            return {"ok": True, "data": result}
        else:
            raise HTTPException(status_code=500, detail="Clockin rewards can only be obtained once within a 24-hour period，you can try later.")
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        user_lock.release()

# 校验是否发放邀请奖励
def checkInviteReward(user_id: str): 
    # 判断用户是否有邀请人
    user_find = Users.get_user_by_id(user_id)
    if user_find.inviter_id is not None and user_find.inviter_id != '':
        #判断用户是否连续三天签到
        reward_list = RewardsTableInstance.get_triduum_history(user_id)
        if len(reward_list) > 2:
            # 更新用户注册奖励
            ## 获取用户注册奖励信息
            rewards_history = RewardsTableInstance.get_create_rewards_by_userid(user_id)
            print("rewards_history", rewards_history)
            # 判断是否有注册奖励
            if rewards_history is not None and rewards_history.invitee is not None and rewards_history.invitee != '':
                ## 获取奖励记录校验是那种奖励
                rewards = RewardsTableInstance.get_rewards_by_invitee(rewards_history.invitee)
                if len(rewards) == 2:
                    inviteReward = next((item for item in rewards if item.reward_type == 'invite' and item.show == True), None)
                    ### 领取邀请奖励
                    if inviteReward is not None and inviteReward.status == False:
                        RewardApiInstance.inviteRewardThread(inviteReward, rewards_history)

# 用户邀请领取奖励
@router.post("/invite_check")
async def invite_check(request: RewardsRequest, user=Depends(get_verified_user)):

    # 获取奖励记录
    rewards_history= RewardsTableInstance.get_rewards_by_id(request.id)
    if rewards_history is None:
        raise HTTPException(status_code=400, detail="You Rewards History not found")

    if rewards_history.reward_type == 'invite':
        if rewards_history.expird == True:
            return {"ok": True, "data": rewards_history}
        if rewards_history.status:
            return {"ok": True, "data": rewards_history}
        else:
            rewards = RewardsTableInstance.get_rewards_by_invitee(rewards_history.invitee)
            if len(rewards) == 2:
                inviteeReward = next((item for item in rewards if item.reward_type == 'new_wallet'), None)
                if inviteeReward is None:
                    raise HTTPException(status_code=400, detail="You Rewards History not found")
                else:
                    if inviteeReward.status and rewards_history.status == False and rewards_history.auto:
                       rewards_history = RewardApiInstance.inviteReward(rewards_history, inviteeReward)
                       return {"ok": True, "data": rewards_history}
                    else:
                       raise HTTPException(status_code=400, detail="Your friend needs to complete the check-in three times.")  
            else:
                raise HTTPException(status_code=400, detail="You Rewards History not found")
    else: 
        raise HTTPException(status_code=400, detail="You Rewards History not found")
    
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

# 获取用户奖励记录
@router.post("/reward_history")
async def get_reward_count(request: RewardsPageRequest,user=Depends(get_verified_user)):
    
    # 查询奖励记录
    rewards_history = RewardsTableInstance.get_rewards_by_user_id(user.id, request.pageNum, request.pageSize)
    for rewards in rewards_history:
        if rewards.reward_type == 'clock_in' and rewards.reward_date.date() != date.today():
            rewards.expird = True
    total = RewardsTableInstance.get_rewards_count_by_user_id(user.id);

    return {
        "row" :rewards_history,
        "total": total
    }

# 获取邀请奖励总数
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

# 同步注册奖励
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
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers = 20) as executor:
                for result in executor.map(send_regist_reward, rewards):
                    results.append(result)
            while len(results) != len(rewards):
                print("=================注册奖励同步进行中=================")
            return {"ok": True, "message": "Success"}
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Failed to received reward")
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        print("====================register_rewards_lock.release==================")
        register_rewards_lock.release()

# 同步邀请奖励
invite_rewards_locks_dict = {}
@router.post("/sync_invite_rewards")
async def sync_invite_rewards(user=Depends(get_verified_user)):
    global invite_rewards_locks_dict
    # 若用户对应的锁不存在，则创建并添加到字典
    invite_rewards_lock =  "system-async-invite-rewards"
    if invite_rewards_lock not in invite_rewards_locks_dict:
        invite_rewards_locks_dict[invite_rewards_lock] = threading.Lock()
    invite_rewards_lock = invite_rewards_locks_dict[invite_rewards_lock]
    invite_rewards_lock.acquire()
    try:
        if user is not None:
            results = []
            rewards = RewardsTableInstance.sync_invite_rewards()
            with concurrent.futures.ThreadPoolExecutor(max_workers = 20) as executor:
                for result in executor.map(send_invite_reward, rewards):
                    results.append(result)
            while len(results) != len(rewards):
                print("=================邀请奖励同步进行中=================")
            return {"ok": True, "message": "Success"}
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Failed to received reward")
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        print("====================register_rewards_lock.release==================")
        invite_rewards_lock.release()

def send_regist_reward(reward: Rewards):
    if reward is not None:
        ## 领取注册奖励
        RewardApiInstance.registReward(reward.id, reward.user_id)

def send_invite_reward(reward: Rewards):
    if reward is not None and reward.invitee is not None and reward.invitee != '':
        ## 获取邀请奖励信息
        rewards = RewardsTableInstance.get_rewards_by_invitee(reward.invitee)
        if len(rewards) == 2:
            inviteReward = None;
            inviteeReward = None;   
            for reward in rewards:
                if reward.reward_type == 'invite':
                    if reward.show:
                        inviteReward = reward
                else:
                    inviteeReward = reward
            ## 领取邀请奖励
            RewardApiInstance.inviteReward(inviteReward, inviteeReward) 
    return reward.id

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
    
@router.get("/dgc_rate")
async def get_dgc_rate(user=Depends(get_verified_user)): 
    # 查询dbc汇率 默认0.00198537(第一次查询的值)
    try:
        dgc_rate = RewardApiInstance.getDgcRate()
        if dgc_rate is not None:
            return dgc_rate
        else:
            return None
    except Exception as e:
        return None
