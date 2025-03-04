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
    user_id = CharField(primary_key=True) # Define string user id
    ip_address = CharField() # Define string IP address
    mac_id = CharField(null=True) # Define string MAC information
    cpu_id = CharField(null=True) # Define string CPU information
    email = CharField(null=True) # Define string email
    captcha_code = CharField(null=True) # Define string image authentication information
    tracking = CharField(null=True) # Define string embedding information
    status = CharField(null=False) # Define KYC authentication status
    created_date = DateTimeField()  # Define integer field creatd_at

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

    # Add KYC records
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
        
    # etrieve records through UserId
    def get_by_userid(self, user_id: str) -> Optional[KycRestrictModel]:
        try:
            kycrestrict = KycRestrict.get_or_none(KycRestrict.user_id == user_id)
            if kycrestrict is None:
                return None
            else:
                kycrestrict_dict = model_to_dict(kycrestrict)  # Convert database objects to dictionaries
                kycrestrict_model = KycRestrictModel(
                    **kycrestrict_dict)  # Convert dictionary to Pydantic model
                return kycrestrict_model
        except Exception as e:
            log.error(f"get_by_userid: {e}")
            return None
        
    # Obtain successful binding records through IP
    def get_by_ip(self, ip_address: str) -> Optional[List[KycRestrictModel]]:
        try:
            # Retrieve data within 10 minutes under the same IP address
            kycrestricts = KycRestrict.select().where((KycRestrict.ip_address == ip_address)
                        & (KycRestrict.status == True))
            kycrestricts_list = [KycRestrictModel(**model_to_dict(kycrestrict)) for kycrestrict in kycrestricts]
            return kycrestricts_list
        except Exception as e:
            log.error(f"get_by_ip: {e}")
            return None
        
    # Verify if the email has been registered before
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
        
    # Update creation time
    def update_date(self, user_id: str, ip_address: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(ip_address=ip_address, captcha_code=None, email=None, created_date=datetime.now()).where(KycRestrict.user_id == user_id)
            query.execute()  # Perform update operation
            # Query updated data
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_date: {e}")
            return None
        
    # Update email records
    def update_email(self, user_id: str, email: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(email=email).where(KycRestrict.user_id == user_id)
            query.execute()  # Perform update operation

            # Query updated data
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # Convert database objects to Pydantic models and return
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_email: {e}")
            return None
        
    # Update captcha_code record
    def update_capcher(self, user_id: str, captcha_code: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(captcha_code=captcha_code).where(KycRestrict.user_id == user_id)
            query.execute()  # Perform update operation

            # Query updated data
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # Convert database objects to Pydantic models and return
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_capcher: {e}")
            return None
    
    # Update buried point data records
    def update_tracking(self, user_id: str, tracking: str) -> Optional[KycRestrictModel]:
        try:
            query = KycRestrict.update(tracking=tracking).where(KycRestrict.user_id == user_id)
            query.execute()  # Perform update operation

            # Query updated data
            kycrestrict = KycRestrict.get(KycRestrict.user_id == user_id)
            # Convert database objects to Pydantic models and return
            return KycRestrictModel(**model_to_dict(kycrestrict))
        except Exception as e:
            log.error(f"update_tracking: {e}")
            return None
        
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
    def remove(self, user_id: str) -> bool:
        try:
            query = KycRestrict.delete().where(KycRestrict.user_id == user_id)
            rows_deleted = query.execute()
            if rows_deleted > 0:
                print(f"KycRestrict is {user_id} The record has been successfully deleted")
                return True
            else:
                print(f"Not found KycRestrict is {user_id} record")
                return False
        except Exception as e:
            log.error(f"update_reward: {e}")
            return False
        
# Initialize KycRestriction table
KycRestrictInstance = KycRestrictTable(DB)