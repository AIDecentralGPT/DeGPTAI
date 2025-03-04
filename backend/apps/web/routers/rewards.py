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

# Verify device ID
async def check_device(user_id: str, device_id: str):
    try:
        user = User.get(User.id == user_id)
        existing_device = Device.get(Device.user == user, Device.device_id == device_id)
        return False  # The device has been registered
    except Device.DoesNotExist:
        Device.create(user=user, device_id=device_id)
        return True  # Device not registered, added

# Verify IP address
async def check_ip(user_id: str, ip_address: str):
    try:
        existing_ip_log = IpLog.get(IpLog.ip_address == ip_address)
        return False  # The IP address has already been used
    except IpLog.DoesNotExist:
        user = User.get(User.id == user_id)
        IpLog.create(user=user, ip_address=ip_address)
        return True  # The IP address has not been used and has been added

# User creates and receives rewards
user_locks_dict = {}
@router.post("/creat_wallet_check")
async def creat_wallet_check(request: RewardsRequest, user=Depends(get_verified_user)):
    global user_locks_dict
    # If the lock corresponding to the user does not exist, create and add it to the dictionary
    if user.id not in user_locks_dict:
        user_locks_dict[user.id + "-new_waller"] = threading.Lock()
    user_lock = user_locks_dict[user.id + "-new_waller"]
    # Retrieve the lock, if the lock is already occupied by another thread of the user, wait
    user_lock.acquire()
    try:
        # Retrieve check-in records
        rewards_history= RewardsTableInstance.get_rewards_by_id(request.id)
        rewards_history.expird = True
        return {"ok": True, "data": rewards_history}
        # if rewards_history is None:
        #     raise HTTPException(status_code=400, detail="You Rewards History not found")
        
        # # Has the verification been collected
        # if rewards_history.status:
        #     return {"ok": True, "data": rewards_history}
        
        # # Verify whether the user has completed KYC authentication
        # user_find = Users.get_user_by_id(user.id)
        # if not user_find.verified:
        #     raise HTTPException(status_code=500, detail="Please complete the KYC verification !")
        
        # # Receive registration rewards
        # rewards_history = RewardApiInstance.registReward(rewards_history.id, rewards_history.user_id)

        # # Determine if there is an invitation reward
        # if rewards_history.invitee is not None and rewards_history.invitee != '':
        #     rewards = RewardsTableInstance.get_rewards_by_invitee(rewards_history.invitee)
        #     if len(rewards) == 2:    
        #         # Receive invitation rewards
        #         inviteReward = next((item for item in rewards if item.reward_type == 'invite' and item.show == True), None)
        #         if inviteReward is not None:
        #             RewardApiInstance.inviteReward(inviteReward, rewards_history)

        # return {"ok": True, "data": rewards_history}
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Failed to received reward")
    finally:
        # Release the lock so that other threads of the user can obtain the lock and execute the method
        user_lock.release()

# User check-in
@router.post("/clock_in")
async def clock_in(user=Depends(get_verified_user)):
    # Get today's date
    today = date.today()
    # Send rewards
    reward_type = "clock_in"
    # Check if the user has already received a reward today
    existing_rewards = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id, today, reward_type)
    print("existing_rewards:", existing_rewards)
    if existing_rewards:
        raise HTTPException(status_code=400, detail="You have received 100 DGC points !")
    
    rewards = RewardsTableInstance.create_reward(user.id, 100, reward_type)
    if rewards is not None:
        # Verify if the user has KYC
        if user.verified:
            # Claim rewards
            RewardApiInstance.dailyReward(rewards.id, user.id)
            # Determine whether to issue invitation rewards
            checkInviteReward(user.id)
        return {"ok": True, "message": "You have received 100 DGC points !"}
    else:
        raise HTTPException(status_code=500, detail="Failed to received reward")

# Users sign in to receive rewards
@router.post("/clock_in_check")
async def clock_in_check(request: RewardsRequest, user=Depends(get_verified_user)):

    global user_locks_dict
    # If the lock corresponding to the user does not exist, create and add it to the dictionary
    if user.id not in user_locks_dict:
        user_locks_dict[user.id + "-clock_in"] = threading.Lock()
    user_lock = user_locks_dict[user.id + "-clock_in"]
    # Retrieve the lock, if the lock is already occupied by another thread of the user, wait
    user_lock.acquire()
    try:
        # Verify whether the user has completed KYC authentication
        user_find = Users.get_user_by_id(user.id)
        if not user_find.verified:
            raise HTTPException(status_code=500, detail="Please complete the KYC verification !")
        
        # Retrieve check-in records
        rewards_history= RewardsTableInstance.get_rewards_by_id(request.id)
        if rewards_history is None:
            raise HTTPException(status_code=400, detail="You Rewards History not found")
        
        # Verify if the reward time has expired
        if rewards_history.reward_date.date() != date.today():
            raise HTTPException(status_code=400, detail="You Rewards History has expired")
        
        # Has the verification been collected
        if rewards_history.status:
            return {"ok": True, "data": rewards_history}
        
        # Claim rewards
        result = RewardApiInstance.dailyReward(rewards_history.id, user.id)
        if result is not None:
            # Determine whether to issue invitation rewards
            checkInviteReward(user.id)
            return {"ok": True, "data": result}
        else:
            raise HTTPException(status_code=500, detail="Clockin rewards can only be obtained once within a 24-hour period，you can try later.")
    finally:
        # Release the lock so that other threads of the user can obtain the lock and execute the method
        user_lock.release()

# Verify if invitation rewards have been issued
def checkInviteReward(user_id: str): 
    # Determine whether the user has an inviter
    user_find = Users.get_user_by_id(user_id)
    if user_find.inviter_id is not None and user_find.inviter_id != '':
        # Determine whether the user has checked in for three consecutive days
        reward_list = RewardsTableInstance.get_triduum_history(user_id)
        if len(reward_list) > 2:
            # Update user registration rewards
            ## Obtain user registration reward information
            rewards_history = RewardsTableInstance.get_create_rewards_by_userid(user_id)
            print("rewards_history", rewards_history)
            # Determine if there are registration rewards available
            if rewards_history is not None and rewards_history.invitee is not None and rewards_history.invitee != '':
                ## What kind of reward is the verification of obtaining reward records
                rewards = RewardsTableInstance.get_rewards_by_invitee(rewards_history.invitee)
                if len(rewards) == 2:
                    inviteReward = next((item for item in rewards if item.reward_type == 'invite' and item.show == True), None)
                    ### Receive invitation rewards
                    if inviteReward is not None and inviteReward.status == False:
                        RewardApiInstance.inviteRewardThread(inviteReward, rewards_history)

# User invitation to receive rewards
@router.post("/invite_check")
async def invite_check(request: RewardsRequest, user=Depends(get_verified_user)):

    # Obtain reward records
    rewards_history= RewardsTableInstance.get_rewards_by_id(request.id)
    if rewards_history is None:
        raise HTTPException(status_code=400, detail="You Rewards History not found")

    if rewards_history.reward_type == 'invite':
        rewards_history.expird = True
        return {"ok": True, "data": rewards_history}
        # if rewards_history.status:
        #     return {"ok": True, "data": rewards_history}
        # else:
        #     rewards = RewardsTableInstance.get_rewards_by_invitee(rewards_history.invitee)
        #     if len(rewards) == 2:
        #         inviteeReward = next((item for item in rewards if item.reward_type == 'new_wallet'), None)
        #         if inviteeReward is None:
        #             raise HTTPException(status_code=400, detail="You Rewards History not found")
        #         else:
        #             if inviteeReward.status:
        #                rewards_history = RewardApiInstance.inviteReward(rewards_history, inviteeReward)
        #                return {"ok": True, "data": rewards_history}
        #             else:
        #                raise HTTPException(status_code=400, detail="Your friend not complete the KYC verification.")  
        #     else:
        #         raise HTTPException(status_code=400, detail="You Rewards History not found")
    else: 
        raise HTTPException(status_code=400, detail="You Rewards History not found")
    
@router.get("/reward_count")
async def get_reward_count(user=Depends(get_verified_user)):
    today = date.today()
    
    # Query the number of times the clock_in type reward has been received
    clock_in_count = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id, today, "clock_in")
    
    # Query the number of times the invite type reward has been received
    invite_count = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id,  today,"invite")

    # Query the number of times the new wallet
    new_wallet = RewardsTableInstance.get_rewards_by_user_id_and_date_and_reward_type(user.id, today, "new_wallet")
    
    return {
        "clock_in": clock_in_count,
        "invite": invite_count,
        "new_wallet": new_wallet
    }

# Obtain user reward records
@router.post("/reward_history")
async def get_reward_count(request: RewardsPageRequest,user=Depends(get_verified_user)):
    
    # Search reward records
    rewards_history = RewardsTableInstance.get_rewards_by_user_id(user.id, request.pageNum, request.pageSize)
    for rewards in rewards_history:
        if rewards.reward_type != 'clock_in':
            rewards.expird = True
        elif rewards.reward_type == 'clock_in' and rewards.reward_date.date() != date.today():
            rewards.expird = True
    total = RewardsTableInstance.get_rewards_count_by_user_id(user.id);

    return {
        "row" :rewards_history,
        "total": total
    }

# Obtain the total number of invitation rewards
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

# Synchronized registration rewards
register_rewards_locks_dict = {}
@router.post("/sync_regist_rewards")
async def sync_regist_rewards(user=Depends(get_verified_user)):
    global register_rewards_locks_dict
    # If the lock corresponding to the user does not exist, create and add it to the dictionary
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
                print("=================Registration reward synchronization in progress=================")
            return {"ok": True, "message": "Success"}
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Failed to received reward")
    finally:
        # Release the lock so that other threads of the user can obtain the lock and execute the method
        print("====================register_rewards_lock.release==================")
        register_rewards_lock.release()

# Synchronize invitation rewards
invite_rewards_locks_dict = {}
@router.post("/sync_invite_rewards")
async def sync_invite_rewards(user=Depends(get_verified_user)):
    global invite_rewards_locks_dict
    # If the lock corresponding to the user does not exist, create and add it to the dictionary
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
                print("=================Invitation reward synchronization in progress=================")
            return {"ok": True, "message": "Success"}
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Failed to received reward")
    finally:
        # Release the lock so that other threads of the user can obtain the lock and execute the method
        print("====================register_rewards_lock.release==================")
        invite_rewards_lock.release()

def send_regist_reward(reward: Rewards):
    if reward is not None:
        ## Receive registration rewards
        RewardApiInstance.registReward(reward.id, reward.user_id)

def send_invite_reward(reward: Rewards):
    if reward is not None and reward.invitee is not None and reward.invitee != '':
        ## Get invitation reward information
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
            ## Receive invitation rewards
            RewardApiInstance.inviteReward(inviteReward, inviteeReward) 
    return reward.id

@router.get("/dbc_rate")
async def get_dbc_rate(user=Depends(get_verified_user)): 
    # Default DBC exchange rate query is 0.00198537 (the value queried for the first time)
    try:
        dbc_rate = RewardApiInstance.getDbcRate()
        if dbc_rate is not None:
            return dbc_rate
        else:
            return 0.0002
    except Exception as e:
        return 0.0002
