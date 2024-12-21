from peewee import *
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional, List
from playhouse.shortcuts import model_to_dict

# 定义 Wallet 表
class Wallet(Model):
    user_id = CharField(primary_key=True)
    amount = FloatField()
    status = BooleanField()

    class Meta:
        database = DB
        table_name = 'wallet'

# 定义 Wallet 的 Pydantic 模型
class WalletModel(BaseModel):
    user_id: str
    amount: float
    status: bool

# 定义 Rewards 操作类
class WalletTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([Wallet])

    # 更新奖励状态    
    def update_wallet(self, user_id: str, status: bool) -> bool:
        try:
            query = Wallet.update(status=status).where(Wallet.user_id==user_id)
            query.execute()  # 执行更新操作

            return True
        except Exception as e:
            return False

    # 通过用户ID获取奖励记录 分页
    def get_wallet_page(self, pageSize: int) -> Optional[List[WalletModel]]:
        try:
            wallets = Wallet.select().where(Wallet.status == False).limit(pageSize)
            return [WalletModel(**model_to_dict(wallet)) for wallet in wallets]
        except Exception as e:
            print("==================", e)
            return None
        
# 初始化 Wallet 表
WalletTableInstance = WalletTable(DB)
