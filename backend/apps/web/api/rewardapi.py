import requests
import json
from typing import Optional
from apps.web.models.rewards import RewardsTableInstance, RewardsModel
import threading

#接口请求地址
#baseUrl = "http://34.234.201.126:8081" # 旧地址
baseUrl = "http://34.234.201.126:8082" # 新地址

RegistAmount = 10000
InviteAmount = 10000
ClockInAmount = 1000

class RewardApi: 

    def __init__(self, url):
        self.apiUrl = url   

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
            data = {"user_id": user_id, "amount": int(reward.reward_amount)}
            # 发送POST请求
            response = requests.post(url, json.dumps(data))
            # 校验请求是否成功
            response.raise_for_status()
            response_json = json.loads(response.text);
            if response_json['code'] == 0:
                # 更新记录
                dgc_hash = response_json['result']['Data']['DGCTxHash']
                result = RewardsTableInstance.update_reward(reward_id, dgc_hash, True, True)
                dbc_hash = response_json['result']['Data']['DBCTxHash']
                RewardsTableInstance.create_dbc_reward(reward.user_id, 0.1, 'new_wallet', dbc_hash, "")
                return result
            else:
                RewardsTableInstance.update_reward(reward_id, None, False, True)
                return None
        except requests.exceptions.HTTPError as e:
            print("===========registReward===========", e)
            return None
        except Exception as e:
            print("===========registReward===========:", e)
            return None

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
        except Exception as e:
            print("===========inviteReward===========", e)
            return None


    # 邀请奖励线程   
    def inviteRewardThread(self, invite: RewardsModel, invitee: RewardsModel):
        thread = threading.Thread(target=self.inviteRewardMore, kwargs={"invite": invite, "invitee": invitee})
        thread.start()

    # 邀请奖励失败做重复执行
    def inviteRewardMore(self, invite: RewardsModel, invitee: RewardsModel):
        if invite is not None:
            result = self.inviteReward(invite, invitee)
            if result is None:
                result = self.inviteReward(invite, invitee)
    
    #每日奖励
    def dailyReward(self, reward_id: str, user_id: str) ->  Optional[RewardsModel]:
        try:
            # 获取记录判断是否已经领取，领取不可再次领取
            reward = RewardsTableInstance.get_rewards_by_id(reward_id)
            if reward.status:
                return reward
            
            #拼接请求地址
            url = f"{self.apiUrl}/claim_daily_rewards"
            #请求体
            data = {"user_id": user_id, "amount": int(reward.reward_amount)}
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