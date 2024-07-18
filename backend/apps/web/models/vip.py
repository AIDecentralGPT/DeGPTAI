from peewee import *
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional
from datetime import date
from peewee import Model, CharField  # 导入Peewee中的Model和CharField
from apps.web.internal.db import DB  # 导入数据库实例DB
from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from typing import List, Union, Optional  # 导入类型提示
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from utils.misc import get_gravatar_url  # 导入获取Gravatar URL的方法
import uuid
import logging
from config import (
    SRC_LOG_LEVELS,
    ENABLE_OPENAI_API,
    OPENAI_API_BASE_URLS,
    OPENAI_API_KEYS,
    CACHE_DIR,
    ENABLE_MODEL_FILTER,
    MODEL_FILTER_LIST,
    AppConfig,
)
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["VIP"])


# --------钱包相关--------
from substrateinterface import Keypair, KeypairType
from substrateinterface.utils.ss58 import ss58_decode
from substrateinterface.utils.hasher import blake2_256
import json
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))  # 使用以太坊主网
# from web3.auto import w3
from eth_account.messages import encode_defunct, _hash_eip191_message
from eth_account import Account




class VIPStatus(Model):
    id = CharField(primary_key=True, default=str(uuid.uuid4))
    user_id = CharField()
    start_date = DateField()
    end_date = DateField()

    class Meta:
        database = DB
        table_name = 'vip_status'





class VIPStatusModel(BaseModel):
    id: str
    user_id: str
    start_date: date
    end_date: date



class VIPStatusTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([VIPStatus])

    def insert_vip_status(self, user_id: str, start_date: date, end_date: date, order_id: str) -> Optional[VIPStatusModel]:
        # order_id = str(uuid.uuid4())
        vip_status = VIPStatusModel(
            id=order_id,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        try:
            result = VIPStatus.create(**vip_status.dict())
            if result:
                return vip_status
            else:
                return None
        except Exception as e:
            log.error(f"insert_vip_status: {e}")
            return None

    def get_vip_status_by_user_id(self, user_id: str) -> Optional[VIPStatusModel]:
        try:
            vip_status = VIPStatus.get(VIPStatus.user_id == user_id)
            return VIPStatusModel(**model_to_dict(vip_status))
        except Exception as e:
            log.error(f"get_vip_status_by_user_id: {e}")
            return None

    def update_vip_end_date(self, user_id: str, new_end_date: date) -> bool:
        try:
            query = VIPStatus.update(end_date=new_end_date).where(VIPStatus.user_id == user_id)
            res = query.execute()
            return res > 0
        except Exception as e:
            log.error(f"update_vip_end_date: {e}")
            return False

    def is_vip_active(self, user_id: str) -> bool:
        try:
            vip_status = self.get_vip_status_by_user_id(user_id)
            if vip_status:
                return vip_status.start_date <= date.today() <= vip_status.end_date
            return False
        except Exception as e:
            log.error(f"is_vip_active: {e}")
            return False
        



VIPStatuses = VIPStatusTable(DB)
