import requests
import json
from typing import Optional
from apps.web.models.rewards import RewardsTableInstance, RewardsModel
import threading

<<<<<<< HEAD
#Interface request address
#baseUrl = "http://34.234.201.126:8081" # Old Address
baseUrl = "http://34.234.201.126:8082" # New Address
=======
#接口请求地址
#baseUrl = "http://34.234.201.126:8081" # 旧地址
baseUrl = "http://34.234.201.126:8082" # 新地址
>>>>>>> fingerprintAuth-out

class RewardApi: 

    def __init__(self, url):
        self.apiUrl = url   

<<<<<<< HEAD
    # Registration Rewards
    def registReward(self, reward_id: str, user_id: str) ->  Optional[RewardsModel]:
        try:
            # Retrieve records to determine if the item has been claimed, but it cannot be claimed again
            reward = RewardsTableInstance.get_rewards_by_id(reward_id)
            if reward.status:
                return reward
            # Splicing request address
            url = f"{self.apiUrl}/claim_register_reward"
            # Request Body
            data = {"user_id": user_id}
            # Send POST request
            response = requests.post(url, json.dumps(data))
            # Verify if the request was successful
            response.raise_for_status()
            # Print response content
            print("===========registReward===========", response.text)
            response_json = json.loads(response.text);
            if response_json['code'] == 0:
                # Update Record
                dgc_hash = response_json['result']['Data']['DGCTxHash']
                result = RewardsTableInstance.update_reward(reward_id, dgc_hash, True)
=======
    #注册奖励
    def registReward(self, reward_id: str, user_id: str) ->  Optional[RewardsModel]:
        try:
            # 获取记录判断是否已经领取，领取不可再次领取
            reward = RewardsTableInstance.get_rewards_by_id(reward_id)
            if reward.status:
                return reward
            #拼接请求地址
            url = f"{self.apiUrl}/claim_register_reward"
            #请求体
            data = {"user_id": user_id}
            # 发送POST请求
            response = requests.post(url, json.dumps(data))
            # 校验请求是否成功
            response.raise_for_status()
            response_json = json.loads(response.text);
            if response_json['code'] == 0:
                # 更新记录
                dgc_hash = response_json['result']['Data']['DGCTxHash']
                result = RewardsTableInstance.update_reward(reward_id, dgc_hash, True, True)
>>>>>>> fingerprintAuth-out
                dbc_hash = response_json['result']['Data']['DBCTxHash']
                RewardsTableInstance.create_dbc_reward(reward.user_id, 0.1, 'new_wallet', dbc_hash, "")
                return result
            else:
<<<<<<< HEAD
                return None
=======
                RewardsTableInstance.update_reward(reward_id, None, False, True)
                return None
        except requests.exceptions.HTTPError as e:
            print("===========registReward===========", e)
            return None
>>>>>>> fingerprintAuth-out
        except Exception as e:
            print("===========registReward===========:", e)
            return None

<<<<<<< HEAD
    # Invitation rewards
    def inviteReward(self, invite: RewardsModel, invitee: RewardsModel) ->  Optional[RewardsModel]:
        try:
            # Retrieve records to determine if the item has been claimed, but it cannot be claimed again
            reward = RewardsTableInstance.get_rewards_by_id(invite.id)
            if reward.status:
                return reward
            # Users receive invitation rewards
            ## Splicing request address
            url = f"{self.apiUrl}/claim_invite_reward"
            ## Request Body
            data = {"inviter_id": invite.user_id, "invitee_id": invitee.user_id, "inviter_amount": int(invite.reward_amount), "invitee_amount": 0}
            print("===========inviteReward-data===========", data)
            ## Send POST request
            response = requests.post(url, json.dumps(data))
            ## Verify if the request was successful
            response.raise_for_status()
            ## Print response content
            print("===========inviteReward===========", response.text)
            response_json = json.loads(response.text)
            if (response_json['code'] == 0):       
                ## Update Record
                return RewardsTableInstance.update_reward(invite.id, response_json['result']['Data']['inviterTxHash'], True)
            else:
                return None
=======
    #邀请奖励
    def inviteReward(self, invite: RewardsModel, invitee: RewardsModel) ->  Optional[RewardsModel]:
        try:
            # 获取记录判断是否已经领取，领取不可再次领取
            reward = RewardsTableInstance.get_rewards_by_id(invite.id)
            if reward.status:
                return reward
            # 用户领取邀请奖励
            ##拼接请求地址
            url = f"{self.apiUrl}/claim_invite_reward"
            ##请求体
            data = {"inviter_id": invite.user_id, "invitee_id": invitee.user_id, "inviter_amount": int(invite.reward_amount), "invitee_amount": 0}
            print("===========inviteReward-data===========", data)
            ## 发送POST请求
            response = requests.post(url, json.dumps(data))
            # 校验请求是否成功
            response.raise_for_status()
            response_json = json.loads(response.text)
            if (response_json['code'] == 0):       
                ## 更新记录
                return RewardsTableInstance.update_reward(invite.id, response_json['result']['Data']['inviterTxHash'], True, True)
            else:
                RewardsTableInstance.update_reward(invite.id, None, False, True)
                return None
        except requests.exceptions.HTTPError as e:
            print("===========inviteReward===========", e)
            return None
>>>>>>> fingerprintAuth-out
        except Exception as e:
            print("===========inviteReward===========", e)
            return None


<<<<<<< HEAD
    # Invite reward thread   
=======
    # 邀请奖励线程   
>>>>>>> fingerprintAuth-out
    def inviteRewardThread(self, invite: RewardsModel, invitee: RewardsModel):
        thread = threading.Thread(target=self.inviteRewardMore, kwargs={"invite": invite, "invitee": invitee})
        thread.start()

<<<<<<< HEAD
    # Invitation reward failed, repeat execution
=======
    # 邀请奖励失败做重复执行
>>>>>>> fingerprintAuth-out
    def inviteRewardMore(self, invite: RewardsModel, invitee: RewardsModel):
        if invite is not None:
            result = self.inviteReward(invite, invitee)
            if result is None:
                result = self.inviteReward(invite, invitee)
    
<<<<<<< HEAD
    # Daily rewards
    def dailyReward(self, reward_id: str, user_id: str) ->  Optional[RewardsModel]:
        try:
            # Retrieve records to determine if the item has been claimed, but it cannot be claimed again
=======
    #每日奖励
    def dailyReward(self, reward_id: str, user_id: str) ->  Optional[RewardsModel]:
        try:
            # 获取记录判断是否已经领取，领取不可再次领取
>>>>>>> fingerprintAuth-out
            reward = RewardsTableInstance.get_rewards_by_id(reward_id)
            if reward.status:
                return reward
            
<<<<<<< HEAD
            # Splicing request address
            url = f"{self.apiUrl}/claim_daily_rewards"
            # Request Body
            data = {"user_id": user_id}
            # Send POST request
            response = requests.post(url, json.dumps(data))
            # Verify if the request was successful
            response.raise_for_status()
            # Print response content
            print("===========dailyReward===========", response.text)
            response_json = json.loads(response.text)
            if response_json['code'] == 0:       
                # Update Record
                tran_hash = response_json['result']['message'].split(':')[1].strip()
                result = RewardsTableInstance.update_reward(reward_id, tran_hash, True)
                return result
            else:
                return None
        except Exception as e:
            print("dailyReward:", e)
            return None

    # Follow Twitter
    def followXReward(self, user_id: str):
        # Splicing request address
        url = f"{self.apiUrl}/claim_followX_reward"
        # Request Body
        data = {"user_id": user_id}
        # Send POST request
        response = requests.post(url, data=json.dumps(data))
        # Print response content
        print(response.text)
        return response

    # Join Tg
    def followTgReward(self, user_id: str):
        # Splicing request address
        url = f"{self.apiUrl}/claim_followTg_reward"
        # Request Body
        data = {"user_id": user_id}
        # Send POST request
        response = requests.post(url, data=json.dumps(data))
        # Print response content
        print(response.text)
        return response
    
    # Obtain DBC exchange rate
=======
            #拼接请求地址
            url = f"{self.apiUrl}/claim_daily_rewards"
            #请求体
            data = {"user_id": user_id}
            # 发送POST请求
            response = requests.post(url, json.dumps(data))
            # 校验请求是否成功
            response.raise_for_status()
            response_json = json.loads(response.text)
            if response_json['code'] == 0:       
                # 更新记录
                tran_hash = response_json['result']['message'].split(':')[1].strip()
                result = RewardsTableInstance.update_reward(reward_id, tran_hash, True, True)
                return result
            else:
                RewardsTableInstance.update_reward(reward_id, None, False, True)
                return None
        except requests.exceptions.HTTPError as e:
            print("===========dailyReward===========", e)
            return None
        except Exception as e:
            print("===========dailyReward===========", e)
            return None

    #关注推特
    def followXReward(self, user_id: str):
        #拼接请求地址
        url = f"{self.apiUrl}/claim_followX_reward"
        #请求体
        data = {"user_id": user_id}
        # 发送POST请求
        response = requests.post(url, data=json.dumps(data))
        # 打印响应内容
        print(response.text)
        return response

    #加入Tg
    def followTgReward(self, user_id: str):
        #拼接请求地址
        url = f"{self.apiUrl}/claim_followTg_reward"
        #请求体
        data = {"user_id": user_id}
        # 发送POST请求
        response = requests.post(url, data=json.dumps(data))
        # 打印响应内容
        print(response.text)
        return response
    
    # 获取dbc汇率
>>>>>>> fingerprintAuth-out
    def getDbcRate(self):
        try:
            rul = "https://dbchaininfo.congtu.cloud/query/dbc_info?language=CN"
            response = requests.get(rul)
            respnose_json = json.loads(response.text)
            print(respnose_json)
            return respnose_json['content']['dbc_price']
        except Exception as e:
            return None
            
        

RewardApiInstance = RewardApi(baseUrl)