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

    class Meta:
        database = DB
        table_name = 'rewards'

# 定义 Rewards 的 Pydantic 模型
class RewardsModel(BaseModel):
    id: str
    user_id: str
    reward_amount: float
    reward_date: date
    reward_type: str
    transfer_hash: str
    invitee: Optional[str] = None

# 定义 Rewards 操作类
class RewardsTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([Rewards])

    def insert_reward(self, user_id: str, reward_amount: float, reward_date: date, reward_type: str, transfer_hash: str, invitee: str) -> Optional[RewardsModel]:
        reward = RewardsModel(
            id=str(uuid.uuid4()),
            user_id=user_id,
            reward_amount=reward_amount,
            reward_date=reward_date,
            reward_type=reward_type,
            transfer_hash=transfer_hash,
            invitee=invitee
        )
        try:
            print(111)
            result = Rewards.create(**reward.model_dump())
            print(222)

            if result:
                return reward
                return None

            else:
              return None
        except Exception as e:
            log.error(f"insert_reward: {e}")
            return None

    def get_rewards_by_user_id(self, user_id: str) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where(Rewards.user_id == user_id)
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_user_id: {e}")
            return None

    def get_rewards_by_user_id_and_date_and_reward_type(self, user_id: str, reward_date: date, reward_type: str) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where((Rewards.user_id == user_id) & (Rewards.reward_date == reward_date)& (Rewards.reward_type == reward_type))
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_user_id_and_date: {e}")
            return None

    def send_reward(self, recipient_address: str, amount: float, reward_type: str, invitee: Optional[str] = None) -> bool:
        try:
            sender_private_key = '0x2cceaca2a5a9823b50c50ef47ca5bc90cc4822c41c01d1c7fac050886fed9be6'
            sender_address = Account.from_key(sender_private_key).address

            nonce = w3.eth.get_transaction_count(sender_address)
            gas_price = w3.eth.gas_price
            gas_limit = 250000  # 增加 gas limit，适用于复杂的合约调用

            # 将amount转换为DGC的最小单位
            amount_wei = w3.to_wei(amount, 'ether')  # 将 amount 转换为 wei 单位

            print("amount", amount, "amount_wei", amount_wei, "w3.eth.chain_id", w3.eth.chain_id)

            # 调用合约的 transfer 函数
            tx = dgc_contract.functions.transfer(
                recipient_address,
                int(amount_wei)
            ).build_transaction({
                'chainId': w3.eth.chain_id,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': nonce,
            })

            # 签名交易
            signed_txn = w3.eth.account.sign_transaction(tx, sender_private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            print('Transaction sent:', tx_hash.hex(), tx_hash.hex())

            # 插入奖励记录
            self.insert_reward(recipient_address, amount, date.today(), reward_type, tx_hash.hex(), invitee)

            return True
        except Exception as e:
            log.error(f"send_reward: {e}")
            print("send_reward:", e)
            return False

# 初始化 Rewards 表
RewardsTableInstance = RewardsTable(DB)
