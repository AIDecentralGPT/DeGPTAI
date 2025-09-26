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

# 初始化Web3
# w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io')) 旧 合约 RPC
w3 = Web3(Web3.HTTPProvider('https://rpc1.dbcwallet.io'))  # 新 合约 RPC
router = APIRouter()

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建 abi.json 文件的绝对路径
abi_path = os.path.join(current_dir, 'abi.json')

# 加载DGC合约的ABI
with open(abi_path, 'r') as abi_file:
    DGC_ABI = json.load(abi_file)

# DGC_TOKEN_CONTRACT_ADDRESS = '0xC260ed583545d036ed99AA5C76583a99B7E85D26'  # 旧 合约地址
# DGC_TOKEN_CONTRACT_ADDRESS = '0x18386F368e7C211E84324337fA8f62d5093272E1'  # 新 合约地址
DGC_TOKEN_CONTRACT_ADDRESS = '0x8E5e4a4d8aE3741DA073303e492B73cb913fb72D'  # 新 合约地址

dgc_contract = w3.eth.contract(
    address=DGC_TOKEN_CONTRACT_ADDRESS, abi=DGC_ABI['abi'])

# 定义 Rewards 表


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
    auto = CharField(null=False)
    expird = CharField(null=False)
    amount_type = CharField()

    class Meta:
        database = DB
        table_name = 'rewards'


class RewardsRequest(BaseModel):
    id: str


class RewardsPageRequest(BaseModel):
    pageSize: int
    pageNum: int

# 定义 Rewards 的 Pydantic 模型


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
    auto: bool = False
    expird: bool = False

# 定义 Rewards 操作类


class RewardsTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([Rewards])

    # 添加奖励记录
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

    # 更新奖励状态
    def update_reward(self, id: str, transfer_hash: str, status: bool, auto: bool) -> Optional[RewardsModel]:
        try:
            query = Rewards.update(
                transfer_hash=transfer_hash, status=status, auto=auto).where(Rewards.id == id)
            query.execute()  # 执行更新操作

            rewards = Rewards.get(Rewards.id == id)  # 查询更新后的用户
            # 将数据库对象转换为Pydantic模型并返回
            return RewardsModel(**model_to_dict(rewards))
        except Exception as e:
            log.error(f"update_reward: {e}")
            return None

    # 通过用户ID获取奖励记录 分页
    def get_rewards_by_user_id(self, user_id: str, pageNum: Optional[int] = 1, pageSize: Optional[int] = 10) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where((Rewards.user_id == user_id) & (Rewards.show == True)
                                             ).order_by(Rewards.reward_date.desc()).paginate(pageNum, pageSize)
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_user_id: {e}")
            return None

    # 通过用户ID获取奖励总数
    def get_rewards_count_by_user_id(self, user_id: str) -> Optional[int]:
        try:
            total = Rewards.select().where((Rewards.user_id == user_id)
                                           & (Rewards.show == True)).count()
            return total
        except Exception as e:
            log.error(f"get_rewards_by_user_id: {e}")
            return 0

    # 通过ID获取奖励信息
    def get_rewards_by_id(self, id: str) -> Optional[RewardsModel]:
        try:
            rewards = Rewards.get_or_none(Rewards.id == id)
            if rewards is None:
                return None
            else:
                rewards_dict = model_to_dict(rewards)  # 将数据库对象转换为字典
                rewards_model = RewardsModel(
                    **rewards_dict)  # 将字典转换为Pydantic模型
                return rewards_model
        except Exception as e:
            log.error(f"get_rewards_by_id: {e}")
            return None

    # 通过用户ID获取用户创建钱包奖励
    def get_create_rewards_by_userid(self, user_id: str) -> Optional[RewardsModel]:
        try:
            rewards = Rewards.get_or_none(
                Rewards.user_id == user_id, Rewards.reward_type == 'new_wallet')
            if rewards is None:
                return None
            else:
                rewards_dict = model_to_dict(rewards)  # 将数据库对象转换为字典
                rewards_model = RewardsModel(
                    **rewards_dict)  # 将字典转换为Pydantic模型
                return rewards_model
        except Exception as e:
            log.error(f"get_rewards_by_id: {e}")
            return None

    # 通过邀请码获取奖励记录
    def get_rewards_by_invitee(self, invitee: str) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where(Rewards.invitee == invitee)
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_id: {e}")
            return None

    # 通过用户ID和奖励类型获取用户某天的奖励信息
    def get_rewards_by_user_id_and_date_and_reward_type(self, user_id: str, reward_date: date, reward_type: str) -> Optional[List[RewardsModel]]:
        try:
            rewards = Rewards.select().where((Rewards.user_id == user_id) & (Rewards.reward_type == reward_type) & (Rewards.show == True)
                                             & (SQL('date(reward_date)') == reward_date))
            return [RewardsModel(**model_to_dict(reward)) for reward in rewards]
        except Exception as e:
            log.error(f"get_rewards_by_user_id_and_date: {e}")
            return None

    # 接口调用创建记录
    def create_reward(self, recipient_address: str, amount: float, reward_type: str, show: Optional[bool] = True, invitee: Optional[str] = None) -> Optional[RewardsModel]:
        try:
            # 插入奖励记录
            rewards = self.insert_reward(recipient_address, amount, datetime.now(
            ), reward_type, "***************", invitee, False, show, "DGC")
            return rewards
        except Exception as e:
            print("create_reward:", e)
            return None

    # 接口调用创建DBC记录
    def create_dbc_reward(self, recipient_address: str, amount: float, reward_type: str, tx_hash: str, invitee: Optional[str] = None) -> Optional[RewardsModel]:
        try:
            # 插入奖励记录
            rewards = self.insert_reward(recipient_address, amount, datetime.now(
            ), reward_type, tx_hash, invitee, True, True, "DBC")
            return rewards
        except Exception as e:
            print("create_dbc_reward:", e)
            return None

    # 指定账户给用户转账DGC
    def send_dgc_reward(self, index: int, recipient_address: str, amount: float) -> str:
        txn_hash = None
        try:
            sender_private_key = ['0x39a2cd7e8425c48367894bb43ef701e0f44edf4942b4444ab0961b2191aa06d7',
                                  '0x9e02e05c71825df2a73ca49da5d4353c27c2a8e5d016e5d8dd03c5a20d6d5895',
                                  '0x4d267b2bf6ed61e8402608c272d1df77377df928a374caa6bff6840fa7973800',
                                  '0x946cb349be26f6c8db7c94f1e75b49662c43a36a742e30deaff0d50a2d90f646',
                                  '0x878459424fe254142b4045e4a8c0b37ddb48f6177c7e23fd5aa387c2389ff6f1',
                                  '0x5cc5f2c56c56fb8e7fb9ef2d3e720337d4f25daa25a94152d8f8769867d403c3',
                                  '0x17edb80023ec4d2e5523b6c8af4726f4eb04a6de47e6d5ebe4faa280734b4b45',
                                  '0xa7cbeaa4fd847a06f39e99bb2ac964ef401e309f5f338e3859cdb9eee8956c6c',
                                  '0x1d4dce74b4744a2075beb00554702438fd985d52ca63a5f13319ae2f4821a96a',
                                  '0x3a5e8b58af86f5b737d7cace0f5e1a15583b3d1b305408f8cbc96f8c91ae8d9c',
                                  '0x4734051a779819fe347f4b1d4e6496170b9b88be35ce2414042d52a3c66f2a3a',
                                  '0xfc8961c66bfccf41d6b58f3213a83c775b11ea6c15aeb92a2ec6b50669cfd488',
                                  '0xcebc4cc3399a78f5d5bde51d29898b5e6de636c56e221f7ec8cda705d70c20da',
                                  '0x8b8bf2e93546eafe50a34182f070cfc82666418eff58405e3055b9437a43db8c',
                                  '0x518a4c3fb16e1dfa65229e82664d34e7ad6e174e45cec05201571a6c5f3cc7f7']
            sender_address = Account.from_key(
                sender_private_key[index]).address

            nonce = w3.eth.get_transaction_count(sender_address)
            gas_price = w3.eth.gas_price
            gas_limit = 400000  # 增加 gas limit，适用于复杂的合约调用

            # 将 amount 转换为 wei 单位
            amount_wei = w3.to_wei(amount, 'ether')

            print(sender_address, recipient_address, amount,
                  "amount_wei", amount_wei, "chain_id", w3.eth.chain_id)

            # 调用合约的 transfer 函数
            tx = dgc_contract.functions.transfer(recipient_address, int(amount_wei)).build_transaction({
                'chainId': w3.eth.chain_id,
                'nonce': nonce,
                'gas': gas_limit,
                'gasPrice': gas_price,
            })

            # 签名交易
            signed_txn = w3.eth.account.sign_transaction(
                tx, sender_private_key[index])
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            txn_hash = tx_hash.hex()

            print("==============dgc=================", txn_hash)

            time.sleep(6)
            receipt = w3.eth.get_transaction_receipt(tx_hash)

            if receipt:
                if receipt['status'] == 1:
                    return {'hash': txn_hash, 'status': True}
                else:
                    return {'hash': txn_hash, 'status': False}
            else:
                return {'hash': txn_hash, 'status': False}

            # 更新记录
            # if reward_id is not None:
            #     result = self.update_reward(reward_id, tx_hash.hex(), True)
            #     return result

        except Exception as e:
            print("send_dgc_reward:", e)
            return {'hash': txn_hash, 'status': False}

    # 指定账户给用户转账DBC
    def send_dbc_reward(self, index: int, recipient_address: str, amount: float) -> str:
        txn_hash = None
        try:
            sender_private_key = ['0x39a2cd7e8425c48367894bb43ef701e0f44edf4942b4444ab0961b2191aa06d7',
                                  '0x9e02e05c71825df2a73ca49da5d4353c27c2a8e5d016e5d8dd03c5a20d6d5895',
                                  '0x4d267b2bf6ed61e8402608c272d1df77377df928a374caa6bff6840fa7973800',
                                  '0x946cb349be26f6c8db7c94f1e75b49662c43a36a742e30deaff0d50a2d90f646',
                                  '0x878459424fe254142b4045e4a8c0b37ddb48f6177c7e23fd5aa387c2389ff6f1',
                                  '0x5cc5f2c56c56fb8e7fb9ef2d3e720337d4f25daa25a94152d8f8769867d403c3',
                                  '0x17edb80023ec4d2e5523b6c8af4726f4eb04a6de47e6d5ebe4faa280734b4b45',
                                  '0xa7cbeaa4fd847a06f39e99bb2ac964ef401e309f5f338e3859cdb9eee8956c6c',
                                  '0x1d4dce74b4744a2075beb00554702438fd985d52ca63a5f13319ae2f4821a96a',
                                  '0x3a5e8b58af86f5b737d7cace0f5e1a15583b3d1b305408f8cbc96f8c91ae8d9c',
                                  '0x4734051a779819fe347f4b1d4e6496170b9b88be35ce2414042d52a3c66f2a3a',
                                  '0xfc8961c66bfccf41d6b58f3213a83c775b11ea6c15aeb92a2ec6b50669cfd488',
                                  '0xcebc4cc3399a78f5d5bde51d29898b5e6de636c56e221f7ec8cda705d70c20da',
                                  '0x8b8bf2e93546eafe50a34182f070cfc82666418eff58405e3055b9437a43db8c',
                                  '0x518a4c3fb16e1dfa65229e82664d34e7ad6e174e45cec05201571a6c5f3cc7f7']
            sender_address = Account.from_key(
                sender_private_key[index]).address

            nonce = w3.eth.get_transaction_count(sender_address)
            gas_price = w3.eth.gas_price
            gas_limit = 21000  # 增加 gas limit，适用于复杂的合约调用

            # 将amount转换为DGC的最小单位
            amount_wei = w3.to_wei(amount, 'ether')  # 将 amount 转换为 wei 单位

            # 组合tx
            tx = {
                'chainId': w3.eth.chain_id,  # 获取当前网络的 chainId
                'nonce': nonce,
                'to': recipient_address,
                'value': amount_wei,
                'gas': gas_limit,  # 标准的以太坊转账 gas 用量
                'gasPrice': gas_price
            }

            # 签名交易
            signed_txn = w3.eth.account.sign_transaction(
                tx, sender_private_key[index])
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            txn_hash = tx_hash.hex()

            print("==============dbc=================", tx_hash.hex())

            time.sleep(6)
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                if receipt['status'] == 1:
                    return {'hash': txn_hash, 'status': True}
                else:
                    return {'hash': txn_hash, 'status': False}
            else:
                return {'hash': txn_hash, 'status': False}

            # 更新记录
            # if reward_id is not None:
            #     result = self.update_reward(reward_id, tx_hash.hex(), True)
            #     return result

        except Exception as e:
            print("send_dbc_reward:", e)
            return {'hash': txn_hash, 'status': False}

    # 校验交易结果
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

    # 获取创建钱包奖励总数
    def get_issue_reward(self) -> int:
        return Rewards.select().where(Rewards.reward_type == "new_wallet", Rewards.amount_type == 'DGC', Rewards.status == True).count()

    # 获取邀请奖励总数
    def get_invitee_total(self) -> int:
        return Rewards.select().where(Rewards.reward_type == "invite", Rewards.show == True).count()

    # 获取邀请奖励应发放总数
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
            print(f"执行查询时出现错误: {e}")
            return 0

    # 获取邀请奖励已发放总数
    def get_issue_invitee_reward_total(self) -> int:
        return Rewards.select().where(Rewards.reward_type == "invite", Rewards.status == True, Rewards.show == True).count()

    # 获取30分钟前KYC已认证未发放的注册奖励
    def sync_regist_rewards(self) -> Optional[List[RewardsModel]]:
        try:
            ten_minutes_ago = datetime.now() - timedelta(minutes=30)
            ten_minutes_ago_str = ten_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')
            sql = f"select r.* from rewards r left join \"user\" u on r.user_id = u.id \
                where r.reward_type = 'new_wallet' and r.status = 'f' and auto = 't' \
                and u.verified = 't' and u.face_time < '{ten_minutes_ago_str}' \
                limit 100"
            rewards = Rewards.raw(sql)
            # 将数据库对象转换为字典并转换为Pydantic模型
            reward_list = [RewardsModel(**model_to_dict(reward))
                           for reward in rewards]
            return reward_list
        except Exception as e:
            print(f"执行查询时出现错误: {e}")
            return None

    # 获取30分钟前KYC已认证未发放的邀请奖励
    def sync_invite_rewards(self) -> Optional[List[RewardsModel]]:
        try:
            ten_minutes_ago = datetime.now() - timedelta(minutes=30)
            ten_minutes_ago_str = ten_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')
            sql = f"select r.* from rewards r left join rewards r2 on r.invitee = r2.invitee \
                and r2.reward_type = 'new_wallet' left join \"user\" u on r2.user_id = u.id \
                and u.verified = 't' and u.face_time < '{ten_minutes_ago_str}' \
                where r.reward_type = 'invite' and r.status = 'f' and r.show = 't' and r.auto= 't' \
                limit 100"
            rewards = Rewards.raw(sql)
            # 将数据库对象转换为字典并转换为Pydantic模型
            reward_list = [RewardsModel(**model_to_dict(reward))
                           for reward in rewards]
            return reward_list
        except Exception as e:
            print(f"执行查询时出现错误: {e}")
            return None

    # 获取用户近三天的签到记录
    def get_triduum_history(self, user_id: str) -> Optional[List[RewardsModel]]:
        try:
            #获取三天前的时间
            three_days_ago = datetime.now() - timedelta(days=2)
            rewards = Rewards.select().where(Rewards.user_id == user_id, Rewards.reward_type == 'clock_in',Rewards.reward_date > three_days_ago.date())
            reward_list = [RewardsModel(**model_to_dict(reward)) for reward in rewards]
            return reward_list
        except Exception as e:
            print(f"执行查询时出现错误: {e}")
            return None 
        
    # 判断用户今天邀请用户是否超过24人
    def get_invitee_today_history(self, user_id: str) -> Optional[List[RewardsModel]]:
        try:
            #获取今天邀请用户数
            reward_date = datetime.now()
            rewards = Rewards.select().where((Rewards.user_id == user_id) & (Rewards.reward_type == 'invite') 
                                    & (SQL('date(reward_date)') == reward_date))
            reward_list = [RewardsModel(**model_to_dict(reward)) for reward in rewards]
            return reward_list
        except Exception as e:
            print(f"执行查询时出现错误: {e}")
            return None 

# 初始化 Rewards 表
RewardsTableInstance = RewardsTable(DB)
