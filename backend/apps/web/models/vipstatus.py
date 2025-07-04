from peewee import *
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional
from datetime import date
from peewee import Model, CharField  # 导入Peewee中的Model和CharField
from apps.web.internal.db import DB  # 导入数据库实例DB
from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from typing import List, Optional  # 导入类型提示
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
import uuid
import logging
from config import ( SRC_LOG_LEVELS )
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["VIP"])


# --------钱包相关--------
from web3 import Web3
#w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))  # 旧以太坊主网
w3 = Web3(Web3.HTTPProvider('https://rpc1.dbcwallet.io')) # 新以太坊主网
# from web3.auto import w3

import time




class VIPStatus(Model):
    id = CharField(primary_key=True, default=str(uuid.uuid4))
    user_id = CharField()
    vip=CharField()
    level=IntegerField()
    type=CharField()
    start_date = DateField()
    end_date = DateField()
    created_at = BigIntegerField()

    class Meta:
        database = DB
        table_name = 'vip_status'


class VIPStatusModel(BaseModel):
    id: str
    user_id: str
    vip: str
    level: int
    type: str
    start_date: date
    end_date: date
    created_at: int

class VIPStatusModelResp(BaseModel):
    id: str
    user_id: str
    vip: str
    level: int
    type: str
    start_date: date
    end_date: date
    created_at: int

# 定义Pydantic模型VipTotalModel
class VipTotalModel(BaseModel):
    vip_total: int = 0  # VIP总数
    expire_total: int = 0  # 过期VIP
    renew_total: int = 0  # 续费VIP



class VIPStatusTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([VIPStatus])

    def insert_vip_status(self, user_id: str, vip: str, level: int, type: str,start_date: date, end_date: date, order_id: str) -> Optional[VIPStatusModel]:
        # order_id = str(uuid.uuid4())
        vip_status = VIPStatusModel(
            id=order_id,
            user_id=user_id,
            vip=vip,
            level=level,
            type=type,
            start_date=start_date,
            end_date=end_date,
            created_at= int(time.time()),
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

    def get_vip_status_by_user_id(self, user_id: str) -> Optional[List[VIPStatusModelResp]]:
        try:
            vip_statuss = VIPStatus.select().where((VIPStatus.user_id == user_id) & 
                (fn.DATE(VIPStatus.start_date) <= date.today()) & (fn.DATE(VIPStatus.end_date) >= date.today())).order_by(VIPStatus.level.desc())
            return [VIPStatusModelResp(**model_to_dict(vip_status)) for vip_status in vip_statuss]
        except Exception as e:
            log.error(f"get_vip_status_by_user_id: {e}")
            return None
        
    def get_vip_status_by_userid_vip(self, user_id: str, vip: str) -> Optional[VIPStatusModelResp]:
        try:
            vip_status = VIPStatus.select().where((VIPStatus.user_id == user_id) & (VIPStatus.vip == vip) &
                (fn.DATE(VIPStatus.start_date) <= date.today()) & (fn.DATE(VIPStatus.end_date) >= date.today())).first()
            return vip_status
        except Exception as e:
            log.error(f"get_vip_status_by_user_id: {e}")
            return None

    def update_vip_end_date(self, id: str, new_end_date: date) -> bool:
        try:
            query = VIPStatus.update(end_date=new_end_date).where(VIPStatus.id == id)
            res = query.execute()
            return res > 0
        except Exception as e:
            log.error(f"update_vip_end_date: {e}")
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
