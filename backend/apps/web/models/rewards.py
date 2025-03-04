import os
from peewee import *
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime, timedelta
import uuid
import logging
from web3 import Web3
from eth_account import Account
from playhouse.shortcuts import model_to_dict
import json
from fastapi import APIRouter
import time

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Initialize Web3
# w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io')) Old Contract RPC
w3 = Web3(Web3.HTTPProvider('https://rpc.dbcwallet.io'))  # New Contract RPC
router = APIRouter()

# Retrieve the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# The absolute path to build the abi. json file
abi_path = os.path.join(current_dir, 'abi.json')

# ABI for loading DGC contract
with open(abi_path, 'r') as abi_file:
    DGC_ABI = json.load(abi_file)

# DGC_TOKEN_CONTRACT_ADDRESS = '0xC260ed583545d036ed99AA5C76583a99B7E85D26'  # Old contract address
DGC_TOKEN_CONTRACT_ADDRESS = '0x18386F368e7C211E84324337fA8f62d5093272E1'  # New contract address

dgc_contract = w3.eth.contract(
    address=DGC_TOKEN_CONTRACT_ADDRESS, abi=DGC_ABI['abi'])

# Define Rewards Table


class Rewards(Model):
    id = CharField(primary_key=True, default=str(uuid.uuid4))
    user_id = CharField()
    reward_amount = FloatField()
    reward_date = DateTimeField()
    reward_type = CharField()
    transfer_hash = CharField()
    invitee = CharField(null=True)
    status = CharField(null=False)
    show = CharField(null=True)
    amount_type = CharField()

    class Meta:
        database = DB
        table_name = 'rewards'


class RewardsRequest(BaseModel):
    id: str


class RewardsPageRequest(BaseModel):
    pageSize: int
    pageNum: int

# Defining the Pydantic Model for Rewards


class RewardsModel(BaseModel):
    id: str
    user_id: str
    reward_amount: float
    reward_date: datetime
    reward_type: str
    transfer_hash: str
    invitee: Optional[str] = None
    status: bool
    show: bool
    amount_type: str
    expird: bool = False

# Define Rewards operation class


class RewardsTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([Rewards])

    # Add reward record
    def insert_reward(self, user_id: str, reward_amount: float, reward_date: datetime, reward_type: str, transfer_hash: str, invitee: str, status: bool, show: bool, amount_type: str) -> Optional[RewardsModel]:
        reward = RewardsModel(
            id=str(uuid.uuid4()),
            user_id=user_id,
            reward_amount=reward_amount,
            reward_date=reward_date,
            reward_type=reward_type,
            transfer_hash=transfer_hash,
            invitee=invitee,
            status=status,
            show=show,
            amount_type=amount_type
        )
        try:
            result = Rewards.create(**reward.model_dump())

            if result:
                return reward
            else:
                return None
        except Exception as e:
            log.error(f"insert_reward: {e}")
            return None

    # Update reward status
    def update_reward(self, id: str, transfer_hash: str, status: bool) -> Optional[RewardsModel]:
        try:
            query = Rewards.update(
                transfer_hash=transfer_hash, status=status).where(Rewards.id == id)
            query.execute()  # Perform update operation

            rewards = Rewards.get(Rewards.id == id)  # Query updated users
            # Convert database objects to Pydantic models and return
            return RewardsModel(**model_to_dict(rewards))
        except Exception as e:
            log.error(f"update_reward: {e}")
            return None

    # Retrieve reward records through user ID pagination
    def get_rewards_by_user_id(self, user_id: str, pageNum: Optional[int] = 1, pageSize: Optional[int] = 10) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where((Rewards.user_id == user_id) & (Rewards.show == True)
                                             ).order_by(Rewards.reward_date.desc()).paginate(pageNum, pageSize)
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_user_id: {e}")
            return None

    # Obtain the total number of rewards through user ID
    def get_rewards_count_by_user_id(self, user_id: str) -> Optional[int]:
        try:
            total = Rewards.select().where((Rewards.user_id == user_id)
                                           & (Rewards.show == True)).count()
            return total
        except Exception as e:
            log.error(f"get_rewards_by_user_id: {e}")
            return 0

    # Obtain reward information through ID
    def get_rewards_by_id(self, id: str) -> Optional[RewardsModel]:
        try:
            rewards = Rewards.get_or_none(Rewards.id == id)
            if rewards is None:
                return None
            else:
                rewards_dict = model_to_dict(rewards)  # Convert database objects to dictionaries
                rewards_model = RewardsModel(
                    **rewards_dict)  # Convert dictionary to Pydantic model
                return rewards_model
        except Exception as e:
            log.error(f"get_rewards_by_id: {e}")
            return None

    # Obtain user created wallet rewards through user ID
    def get_create_rewards_by_userid(self, user_id: str) -> Optional[RewardsModel]:
        try:
            rewards = Rewards.get_or_none(
                Rewards.user_id == user_id, Rewards.reward_type == 'new_wallet')
            if rewards is None:
                return None
            else:
                rewards_dict = model_to_dict(rewards)  # Convert database objects to dictionaries
                rewards_model = RewardsModel(
                    **rewards_dict)  # Convert dictionary to Pydantic model
                return rewards_model
        except Exception as e:
            log.error(f"get_rewards_by_id: {e}")
            return None

    # Obtain reward records through invitation codes
    def get_rewards_by_invitee(self, invitee: str) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where(Rewards.invitee == invitee)
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_id: {e}")
            return None

    # Obtain the reward information of a user for a certain day through their user ID and reward type
    def get_rewards_by_user_id_and_date_and_reward_type(self, user_id: str, reward_date: date, reward_type: str) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where((Rewards.user_id == user_id) & (Rewards.reward_type == reward_type) & (Rewards.show == True)
                                             & (SQL('date(reward_date)') == reward_date))
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_user_id_and_date: {e}")
            return None

    # Interface call creation record
    def create_reward(self, recipient_address: str, amount: float, reward_type: str, show: Optional[bool] = True, invitee: Optional[str] = None) -> Optional[RewardsModel]:
        try:
            # Insert reward record
            rewards = self.insert_reward(recipient_address, amount, datetime.now(
            ), reward_type, "***************", invitee, False, show, "DGC")
            return rewards
        except Exception as e:
            print("create_reward:", e)
            return None

    # API call to create DBC record
    def create_dbc_reward(self, recipient_address: str, amount: float, reward_type: str, tx_hash: str, invitee: Optional[str] = None) -> Optional[RewardsModel]:
        try:
            # Insert reward record
            rewards = self.insert_reward(recipient_address, amount, datetime.now(
            ), reward_type, tx_hash, invitee, True, True, "DBC")
            return rewards
        except Exception as e:
            print("create_dbc_reward:", e)
            return None

    # Verify transaction results
    def check_reward(self, tx_hash: str) -> Optional[bool]:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                if receipt['status'] == 1:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False

    # Obtain the total number of rewards for creating wallets
    def get_issue_reward(self) -> int:
        return Rewards.select().where(Rewards.reward_type == "new_wallet", Rewards.amount_type == 'DGC', Rewards.status == True).count()

    # Obtain the total number of invitation rewards
    def get_invitee_total(self) -> int:
        return Rewards.select().where(Rewards.reward_type == "invite", Rewards.show == True).count()

    # Total number of invitation rewards to be distributed
    def get_invitee_reward_total(self) -> int:
        try:
            sql = "select count(r.*) as count from rewards r \
                left join rewards r2 on r.invitee = r2.invitee \
                left join \"user\" u on r2.user_id = u.id \
                where r.reward_type = 'invite' and r.\"show\" = 't' \
                and r2.reward_type = 'new_wallet' and u.verified = 't'"
            results = Rewards.raw(sql).dicts()
            if len(results) > 0:
                return results[0]['count']
            return 0
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return 0

    # Total number of invitation rewards issued
    def get_issue_invitee_reward_total(self) -> int:
        return Rewards.select().where(Rewards.reward_type == "invite", Rewards.status == True, Rewards.show == True).count()

    # Get registration rewards that have been KYC verified but not yet issued 30 minutes ago
    def sync_regist_rewards(self) -> Optional[List[RewardsModel]]:
        try:
            ten_minutes_ago = datetime.now() - timedelta(minutes=30)
            ten_minutes_ago_str = ten_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')
            sql = f"select r.* from rewards r left join \"user\" u on r.user_id = u.id \
                where r.reward_type = 'new_wallet' and r.status = 'f' \
                and u.verified = 't' and u.face_time < '{ten_minutes_ago_str}' \
                limit 100"
            rewards = Rewards.raw(sql)
            # Convert database objects into dictionaries and Pydantic models
            reward_list = [RewardsModel(**model_to_dict(reward))
                           for reward in rewards]
            return reward_list
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return None

    # Get invitation rewards for KYC verified but not yet issued 30 minutes ago
    def sync_invite_rewards(self) -> Optional[List[RewardsModel]]:
        try:
            ten_minutes_ago = datetime.now() - timedelta(minutes=30)
            ten_minutes_ago_str = ten_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')
            sql = f"select r.* from rewards r left join rewards r2 on r.invitee = r2.invitee \
                and r2.reward_type = 'new_wallet' left join \"user\" u on r2.user_id = u.id \
                and u.verified = 't' and u.face_time < '{ten_minutes_ago_str}' \
                where r.reward_type = 'invite' and r.status = 'f' and r.show = 't' \
                limit 100"
            rewards = Rewards.raw(sql)
            # Convert database objects into dictionaries and Pydantic models
            reward_list = [RewardsModel(**model_to_dict(reward))
                           for reward in rewards]
            return reward_list
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return None

    # Retrieve the user's check-in records for the past three days
    def get_triduum_history(self, user_id: str) -> Optional[List[RewardsModel]]:
        try:
            # Get the time three days ago
            three_days_ago = datetime.now() - timedelta(days=2)
            rewards = Rewards.select().where(Rewards.user_id == user_id, Rewards.reward_date > three_days_ago)
            reward_list = [RewardsModel(**model_to_dict(reward)) for reward in rewards]
            return reward_list
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return None 
        
    # Get the number of invited users for today
    def get_invitee_today_history(self, user_id: str) -> Optional[List[RewardsModel]]:
        try:
            # Get the number of invited users for today
            reward_date = datetime.now()
            rewards = Rewards.select().where((Rewards.user_id == user_id) & (Rewards.reward_type == 'invite') 
                                    & (SQL('date(reward_date)') == reward_date))
            reward_list = [RewardsModel(**model_to_dict(reward)) for reward in rewards]
            return reward_list
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return None 

# Initialize the Rewards table
RewardsTableInstance = RewardsTable(DB)
