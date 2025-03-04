from peewee import *
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional
from datetime import date
from peewee import Model, CharField
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import List, Union, Optional
from playhouse.shortcuts import model_to_dict
from utils.misc import get_gravatar_url
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


# --------Wallet related--------
from substrateinterface import Keypair, KeypairType
from substrateinterface.utils.ss58 import ss58_decode
from substrateinterface.utils.hasher import blake2_256
import json
from web3 import Web3
#w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))  # Old Ethereum mainnet
w3 = Web3(Web3.HTTPProvider('https://rpc.dbcwallet.io')) # New Ethereum mainnet
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

class VIPStatusModelResp(BaseModel):
    id: str
    user_id: str
    start_date: date
    end_date: date
    is_pro: Optional[bool] = None


# Define the Pydantic model VipTotalModel
class VipTotalModel(BaseModel):
    vip_total: int = 0  # Total number of VIP
    expire_total: int = 0  # Expired VIP
    renew_total: int = 0  # Renewal VIP



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

    def get_vip_status_by_user_id(self, user_id: str) -> Optional[VIPStatusModelResp]:
        try:
            vip_status = VIPStatus.select().where(VIPStatus.user_id == user_id).order_by(-VIPStatus.end_date).limit(1).get()
            if (vip_status):
                return VIPStatusModelResp(**model_to_dict(vip_status))
            else:
                return None
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
    
    def get_vip_total(self) -> Optional[VipTotalModel]:
        vip_total = VIPStatus.select(VIPStatus.user_id, fn.Max(VIPStatus.end_date).alias('end_date')).group_by(VIPStatus.user_id).count()
        expire_total = VIPStatus.select(VIPStatus.user_id, fn.Max(VIPStatus.end_date).alias('end_date')).where(VIPStatus.end_date < date.today()).group_by(VIPStatus.user_id).count()
        renew_total = VIPStatus.select(fn.COUNT(VIPStatus.user_id)).group_by(VIPStatus.user_id).having(fn.COUNT(VIPStatus.user_id) > 1).count()
        data = {    
            "vip_total": vip_total,
            "expire_total": expire_total,
            "renew_total": renew_total
        }
        return VipTotalModel(**data)



VIPStatuses = VIPStatusTable(DB)
