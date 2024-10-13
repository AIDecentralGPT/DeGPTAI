from peewee import *
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
import uuid
import logging
from web3 import Web3
from eth_account import Account
from playhouse.shortcuts import model_to_dict
import json
from fastapi import APIRouter

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# 初始化Web3
w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))
router = APIRouter()
import os

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建 abi.json 文件的绝对路径
abi_path = os.path.join(current_dir, 'abi.json')

# 加载DGC合约的ABI
with open(abi_path, 'r') as abi_file:
    DGC_ABI = json.load(abi_file)

DGC_TOKEN_CONTRACT_ADDRESS = '0x82b1a3d719dDbFDa07AD1312c3063a829e1e66F1'  # 替换为实际地址
dgc_contract = w3.eth.contract(address=DGC_TOKEN_CONTRACT_ADDRESS, abi=DGC_ABI['abi'])

# 定义 Rewards 表
class Rewards(Model):
    id = CharField(primary_key=True, default=str(uuid.uuid4))
    user_id = CharField()
    reward_amount = FloatField()
    reward_date = DateField()
    reward_type = CharField()
    transfer_hash = CharField()
    invitee = CharField(null=True)
    status = CharField()

    class Meta:
        database = DB
        table_name = 'rewards'

class RewardsRequest(BaseModel):
    id: str

# 定义 Rewards 的 Pydantic 模型
class RewardsModel(BaseModel):
    id: str
    user_id: str
    reward_amount: float
    reward_date: date
    reward_type: str
    transfer_hash: str
    invitee: Optional[str] = None
    status: bool

# 定义 Rewards 操作类
class RewardsTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([Rewards])

    def insert_reward(self, user_id: str, reward_amount: float, reward_date: date, reward_type: str, transfer_hash: str, invitee: str, status: bool) -> Optional[RewardsModel]:
        reward = RewardsModel(
            id=str(uuid.uuid4()),
            user_id=user_id,
            reward_amount=reward_amount,
            reward_date=reward_date,
            reward_type=reward_type,
            transfer_hash=transfer_hash,
            invitee=invitee,
            status=status
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
        
    def update_reward(self, id: str, transfer_hash: str, status: bool) -> Optional[RewardsModel]:
        try:
            query = Rewards.update(transfer_hash=transfer_hash, status=status).where(Rewards.id==id)
            query.execute()  # 执行更新操作

            rewards = Rewards.get(Rewards.id == id)  # 查询更新后的用户
            return RewardsModel(**model_to_dict(rewards))  # 将数据库对象转换为Pydantic模型并返回
        except Exception as e:
            log.error(f"update_reward: {e}")
            return None

    def get_rewards_by_user_id(self, user_id: str) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where(Rewards.user_id == user_id)
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_user_id: {e}")
            return None
    
    def get_rewards_by_id(self, id: str, user_id: str) -> Optional[RewardsModel]:
        try:
            rewards = Rewards.get_or_none(Rewards.id == id, Rewards.user_id == user_id)
            if rewards is None:
                return None
            else:
                rewards_dict = model_to_dict(rewards)  # 将数据库对象转换为字典
                rewards_model = RewardsModel(**rewards_dict)  # 将字典转换为Pydantic模型
                return rewards_model
        except Exception as e:
            log.error(f"get_rewards_by_id: {e}")
            return None

    def get_rewards_by_user_id_and_date_and_reward_type(self, user_id: str, reward_date: date, reward_type: str) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where((Rewards.user_id == user_id) & (Rewards.reward_date == reward_date)& (Rewards.reward_type == reward_type))
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_user_id_and_date: {e}")
            return None
        
    def create_reward(self, recipient_address: str, amount: float, reward_type: str, invitee: Optional[str] = None) -> bool:
        try:
            # 插入奖励记录
            self.insert_reward(recipient_address, amount, date.today(), reward_type, "**********", invitee, False)
            return True
        except Exception as e:
            print("send_reward:", e)
            return False

    def send_reward(self, reward_id: str, recipient_address: str, amount: float, reward_type: str) ->  Optional[RewardsModel]:
        try:
            sender_private_key = '0xdbee5204091639ded19bef844221ac09216a56cee27682451e288e9b50853ce3'
            sender_address = Account.from_key(sender_private_key).address

            nonce = w3.eth.get_transaction_count(sender_address)
            gas_price = w3.eth.gas_price
            gas_limit = 250000  # 增加 gas limit，适用于复杂的合约调用

            # 将amount转换为DGC的最小单位
            amount_wei = w3.to_wei(amount, 'ether')  # 将 amount 转换为 wei 单位

            print("amount", amount, "amount_wei", amount_wei, "w3.eth.chain_id", w3.eth.chain_id)

            # 调用合约的 transfer 函数
            tx = dgc_contract.functions.transfer(recipient_address, int(amount_wei)).build_transaction({
                # 'chainId': w3.eth.chain_id,
                'from': sender_address,
                'nonce': nonce,
                'gas': gas_limit,
                'gasPrice': gas_price,
            })

            # 签名交易
            signed_txn = w3.eth.account.sign_transaction(tx, sender_private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            # 更新记录
            result = self.update_reward(reward_id, tx_hash.hex(), True)
            return result
        
        except Exception as e:
            print("send_reward:", e)
            return None

# 初始化 Rewards 表
RewardsTableInstance = RewardsTable(DB)
