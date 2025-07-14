from peewee import *
from apps.web.internal.db import DB
from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime, timedelta
from playhouse.shortcuts import model_to_dict
from apps.web.api.captcha import CaptchaApiInstance
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class KycRestrict(Model):
<<<<<<< HEAD
    user_id = CharField(primary_key=True) # Define string user id
    ip_address = CharField() # Define string IP address
    mac_id = CharField(null=True) # Define string MAC information
    cpu_id = CharField(null=True) # Define string CPU information
    email = CharField(null=True) # Define string email
    captcha_code = CharField(null=True) # Define string image authentication information
    tracking = CharField(null=True) # Define string embedding information
    status = CharField(null=False) # Define KYC authentication status
    created_date = DateTimeField()  # Define integer field creatd_at
=======
    user_id = CharField(primary_key=True) # 定义字符串用户ID
    ip_address = CharField() # 定义字符串IP地址
    mac_id = CharField(null=True) # 定义字符串MAC信息
    cpu_id = CharField(null=True) # 定义字符串CPU信息
    email = CharField(null=True) # 定义字符串email
    captcha_code = CharField(null=True) # 定义字符串图片认证信息
    tracking = CharField(null=True) # 定义字符串埋点信息
    status = CharField(null=False) # 定义大KYC认证状态
    created_date = DateTimeField()  # 定义大整数字段created_at
>>>>>>> fingerprintAuth-out

    class Meta:
        database = DB
        table_name = 'kyc_restrict'

class KycRestrictModel(BaseModel):
    user_id: str
    ip_address: str
    mac_id: Optional[str] = None
    cpu_id: Optional[str] = None
    email: Optional[str] = None
    captcha_code: Optional[str] = None
    tracking: Optional[str] = None
    status: bool
    created_date: datetime

class CheckKycRequest(BaseModel):
    mac_id: str
    cpu_id: str

class BindEmailRequest(BaseModel):
    email: str

class BindCaptchaRequest(BaseModel):
    captcha_code: str

class BindTrackingRequest(BaseModel):
    tracking: str

class KycRestrictTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([KycRestrict])

<<<<<<< HEAD
    # Add KYC records
=======
    # 添加KYC记录
>>>>>>> fingerprintAuth-out
    def insert(self, user_id: str, ip_address: str, mac_id: str, cpu_id: str) -> Optional[KycRestrictModel]:
        kycrestrict = KycRestrictModel(
            user_id=user_id,
            ip_address=ip_address,
            mac_id=mac_id,
            cpu_id=cpu_id,
            email=None,
            captcha_code=None,
            tracking=None,
            status=False,
            created_date=datetime.now()
        )
        try:
            result = KycRestrict.create(**kycrestrict.model_dump())
            if result:
                return kycrestrict
            else:
                return None
        except Exception as e:
            log.error(f"insert_kycrestrict: {e}")
            return None
        
<<<<<<< HEAD
    # etrieve records through UserId
=======
    # 通过UserId获取记录
>>>>>>> fingerprintAuth-out
    def get_by_userid(self, user_id: str) -> Optional[KycRestrictModel]:
        try:
            kycrestrict = KycRestrict.get_or_none(KycRestrict.user_id == user_id)
            if kycrestrict is None:
                return None
            else:
<<<<<<< HEAD
                kycrestrict_dict = model_to_dict(kycrestrict)  # Convert database objects to dictionaries
                kycrestrict_model = KycRestrictModel(
                    **kycrestrict_dict)  # Convert dictionary to Pydantic model
=======
                kycrestrict_dict = model_to_dict(kycrestrict)  # 将数据库对象转换为字典
                kycrestrict_model = KycRestrictModel(
                    **kycrestrict_dict)  # 将字典转换为Pydantic模型
>>>>>>> fingerprintAuth-out
                return kycrestrict_model
        except Exception as e:
            log.error(f"get_by_userid: {e}")
            return None
        
<<<<<<< HEAD
    # Obtain successful binding records through IP
    def get_by_ip(self, ip_address: str) -> Optional[List[KycRestrictModel]]:
        try:
            # Retrieve data within 10 minutes under the same IP address
=======
    # 通过IP获取绑定成功记录
    def get_by_ip(self, ip_address: str) -> Optional[List[KycRestrictModel]]:
        try:
            # 获取同已IP下10分钟之内的数据
>>>>>>> fingerprintAuth-out
            kycrestricts = KycRestrict.select().where((KycRestrict.ip_address == ip_address)
                        & (KycRestrict.status == True))
            kycrestricts_list = [KycRestrictModel(**model_to_dict(kycrestrict)) for kycrestrict in kycrestricts]
            return kycrestricts_list
        except Exception as e:
            log.error(f"get_by_ip: {e}")
            return None
        
<<<<<<< HEAD
    # Verify if the email has been registered before
=======
    # 校验email是否已注册过
>>>>>>> fingerprintAuth-out
    def check_email(self, email: str) -> bool:
        try:
            kycrestricts = KycRestrict.select().where(KycRestrict.email == email, KycRestrict.status == True)
            kycrestrict_list = [KycRestrictModel(**model_to_dict(kycrestrict)) for kycrestrict in kycrestricts]
            if kycrestrict_list is not None and len(kycrestrict_list) > 0:
                return True
            else:
                return False
        except Exception as e:
            log.error(f"get_by_ip: {e}")
            return False
        
<<<<<<< HEAD
    # Update creation time
    def update_date(self, user_id: str, ip_address: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(ip_address=ip_address, captcha_code=None, email=None, created_date=datetime.now()).where(KycRestrict.user_id == user_id)
            query.execute()  # Perform update operation
            # Query updated data
=======
    # 更新创建时间
    def update_date(self, user_id: str, ip_address: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(ip_address=ip_address, captcha_code=None, email=None, created_date=datetime.now()).where(KycRestrict.user_id == user_id)
            query.execute()  # 执行更新操作
            # 查询更新后数据
>>>>>>> fingerprintAuth-out
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_date: {e}")
            return None
        
<<<<<<< HEAD
    # Update email records
    def update_email(self, user_id: str, email: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(email=email).where(KycRestrict.user_id == user_id)
            query.execute()  # Perform update operation

            # Query updated data
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # Convert database objects to Pydantic models and return
=======
    # 更新email记录
    def update_email(self, user_id: str, email: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(email=email).where(KycRestrict.user_id == user_id)
            query.execute()  # 执行更新操作

            # 查询更新后数据
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # 将数据库对象转换为Pydantic模型并返回
>>>>>>> fingerprintAuth-out
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_email: {e}")
            return None
        
<<<<<<< HEAD
    # Update captcha_code record
    def update_capcher(self, user_id: str, captcha_code: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(captcha_code=captcha_code).where(KycRestrict.user_id == user_id)
            query.execute()  # Perform update operation

            # Query updated data
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # Convert database objects to Pydantic models and return
=======
    # 更新captcha_code记录
    def update_capcher(self, user_id: str, captcha_code: str, client_ip: str) -> Optional[KycRestrictModel]:
        try:
            kycrestrict = KycRestrict.get_or_none(KycRestrict.user_id == user_id)
            if kycrestrict is not None:
                query = KycRestrict.update(captcha_code=captcha_code).where(KycRestrict.user_id == user_id)
                query.execute()  # 执行更新操作
            else:
                kycrestrict = KycRestrictModel(
                    user_id=user_id,
                    ip_address=client_ip,
                    mac_id=None,
                    cpu_id=None,
                    email=None,
                    captcha_code=captcha_code,
                    tracking=None,
                    status=False,
                    created_date=datetime.now()
                )
                KycRestrict.create(**kycrestrict.model_dump())

            query = KycRestrict.update(captcha_code=captcha_code).where(KycRestrict.user_id == user_id)
            query.execute()  # 执行更新操作

            # 查询更新后数据
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # 将数据库对象转换为Pydantic模型并返回
>>>>>>> fingerprintAuth-out
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_capcher: {e}")
            return None
    
<<<<<<< HEAD
    # Update buried point data records
    def update_tracking(self, user_id: str, tracking: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(tracking=tracking).where(KycRestrict.user_id == user_id)
            query.execute()  # Perform update operation

            # Query updated data
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # Convert database objects to Pydantic models and return
=======
    # 更新埋点数据记录
    def update_tracking(self, user_id: str, tracking: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(tracking=tracking).where(KycRestrict.user_id == user_id)
            query.execute()  # 执行更新操作

            # 查询更新后数据
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # 将数据库对象转换为Pydantic模型并返回
>>>>>>> fingerprintAuth-out
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_tracking: {e}")
            return None
        
<<<<<<< HEAD
    # Update KYC authentication results
    def update_kyc(self, user_id: str, status: bool) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(status=status).where(KycRestrict.user_id == user_id)
            query.execute()  # Perform update operation

            # Query updated data
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # Convert database objects to Pydantic models and return
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_reward: {e}")
            return None
        
    # Remove KYC authentication results
=======
    # 更新kyc认证结果
    def update_kyc(self, user_id: str, status: bool) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(status=status).where(KycRestrict.user_id == user_id)
            query.execute()  # 执行更新操作

            # 查询更新后数据
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # 将数据库对象转换为Pydantic模型并返回
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_kyc: {e}")
            return None
        
    # 移除kyc认证结果
>>>>>>> fingerprintAuth-out
    def remove(self, user_id: str) -> bool:
        try:
            query = KycRestrict.delete().where(KycRestrict.user_id == user_id)
            rows_deleted = query.execute()
            if rows_deleted > 0:
<<<<<<< HEAD
                print(f"KycRestrict is {user_id} The record has been successfully deleted")
                return True
            else:
                print(f"Not found KycRestrict is {user_id} record")
                return False
        except Exception as e:
            log.error(f"update_reward: {e}")
            return False
        
# Initialize KycRestriction table
=======
                print(f"KycRestrict 为 {user_id} 的记录已成功删除")
                return True
            else:
                print(f"未找到 KycRestrict 为 {user_id} 的记录")
                return False
        except Exception as e:
            log.error(f"remove_kyc: {e}")
            return False
        
# 初始化 KycRestrict 表
>>>>>>> fingerprintAuth-out
KycRestrictInstance = KycRestrictTable(DB)