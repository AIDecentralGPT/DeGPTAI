from peewee import *
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional, List
from playhouse.shortcuts import model_to_dict

# 定义 Wallet 表
class Wallet(Model):
    user_id = CharField(primary_key=True)
    dgc_amount = FloatField()
    dbc_amount = FloatField()
    dgc_hash = CharField(null=True)
    dbc_hash = CharField(null=True)
    dgc_status = BooleanField()
    dbc_status = BooleanField()

    class Meta:
        database = DB
        table_name = 'wallet_user'

# 定义 Wallet 的 Pydantic 模型
class WalletModel(BaseModel):
    user_id: str
    dgc_amount: float
    dbc_amount: float
    dgc_hash: Optional[str] = None
    dbc_hash: Optional[str] = None
    dgc_status: bool
    dbc_status: bool

# 定义 Rewards 操作类
class WalletTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([Wallet])

    # 批量添加用户余额
    def batch_wallet(self, wallets: List[WalletModel]) -> bool:
        try:
            Wallet.insert_many(wallets).execute()
            return True
        except Exception as e:
            print("=======================", e)
            return False

    # 更新DGC奖励状态    
    def update_wallet_dgc(self, user_id: str, dgc_hash: str, dgc_status: bool) -> bool:
        try:
            query = Wallet.update(dgc_hash=dgc_hash, dgc_status=dgc_status).where(Wallet.user_id==user_id)
            query.execute()  # 执行更新操作

            return True
        except Exception as e:
            return False
        
    # 更新DBC奖励状态    
    def update_wallet_dbc(self, user_id: str, dbc_hash: str, dbc_status: bool) -> bool:
        try:
            query = Wallet.update(dbc_hash=dbc_hash, dbc_status=dbc_status).where(Wallet.user_id==user_id)
            query.execute()  # 执行更新操作

            return True
        except Exception as e:
            return False

    # 通过用户ID获取DGC奖励记录 分页
    def get_wallet_dgc_page(self, pageSize: int) -> Optional[List[WalletModel]]:
        try:
            wallets = Wallet.select().where(Wallet.dgc_status == False).limit(pageSize)
            return [WalletModel(**model_to_dict(wallet)) for wallet in wallets]
        except Exception as e:
            print("==================", e)
            return None
        
     # 通过用户ID获取DBC奖励记录 分页
    def get_wallet_dbc_page(self, pageSize: int) -> Optional[List[WalletModel]]:
        try:
            wallets = Wallet.select().where(Wallet.dbc_status == False).limit(pageSize)
            return [WalletModel(**model_to_dict(wallet)) for wallet in wallets]
        except Exception as e:
            print("==================", e)
            return None
        
# 初始化 Wallet 表
WalletTableInstance = WalletTable(DB)
