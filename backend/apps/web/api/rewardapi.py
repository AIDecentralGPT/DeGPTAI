import requests
import json
from typing import Optional
from apps.web.models.rewards import RewardsTableInstance, RewardsModel
import threading

#Interface request address
#baseUrl = "http://34.234.201.126:8081" # Old Address
baseUrl = "http://34.234.201.126:8082" # New Address

class RewardApi: 

    def __init__(self, url):
        self.apiUrl = url   

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
                dbc_hash = response_json['result']['Data']['DBCTxHash']
                RewardsTableInstance.create_dbc_reward(reward.user_id, 0.1, 'new_wallet', dbc_hash, "")
                return result
            else:
                return None
        except Exception as e:
            print("===========registReward===========:", e)
            return None

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
        except Exception as e:
            print("===========inviteReward===========", e)
            return None


    # Invite reward thread   
    def inviteRewardThread(self, invite: RewardsModel, invitee: RewardsModel):
        thread = threading.Thread(target=self.inviteRewardMore, kwargs={"invite": invite, "invitee": invitee})
        thread.start()

    # Invitation reward failed, repeat execution
    def inviteRewardMore(self, invite: RewardsModel, invitee: RewardsModel):
        if invite is not None:
            result = self.inviteReward(invite, invitee)
            if result is None:
                result = self.inviteReward(invite, invitee)
    
    # Daily rewards
    def dailyReward(self, reward_id: str, user_id: str) ->  Optional[RewardsModel]:
        try:
            # Retrieve records to determine if the item has been claimed, but it cannot be claimed again
            reward = RewardsTableInstance.get_rewards_by_id(reward_id)
            if reward.status:
                return reward
            
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