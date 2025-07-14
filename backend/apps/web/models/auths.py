from pydantic import BaseModel
from typing import List, Union, Optional, Tuple as TypingTuple
from datetime import datetime
import time
import uuid
import logging
from peewee import *



from apps.web.models.users import UserModel, Users
from utils.utils import verify_password

from apps.web.internal.db import DB

from config import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# DB MODEL
####################


class Auth(Model):
    id = CharField(unique=True)
    email = CharField()
    password = TextField()
    active = BooleanField()


    class Meta:
        database = DB


class AuthModel(BaseModel):
    id: str
    email: str
    password: str
    active: bool = True


####################
# Forms
####################


class Token(BaseModel):
    token: str
    token_type: str


class ApiKey(BaseModel):
    api_key: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    profile_image_url: str
    address_type: Optional[str] = None
    verified: Optional[bool] = None
    address: Optional[str] = None


class SigninResponse(Token, UserResponse):
    pass





class FingerprintSigninResponse(Token, UserResponse):
    pass

class SigninForm(BaseModel):
    email: str
    password: str
    visiter_id: Optional[str] = None


class WalletSigninForm(BaseModel):
    address: str
    address_type: str
    nonce:str
    signature: str
    device_id: str
    private_key: Optional[str] = None
    inviter_id: Optional[str] = None
    channel: Optional[str] = None


class FingerprintSignInForm(BaseModel):
    id: str
    channel: str


class ProfileImageUrlForm(BaseModel):
    profile_image_url: str


class UpdateProfileForm(BaseModel):
    profile_image_url: str
    name: str


class UpdatePasswordForm(BaseModel):
    password: str
    new_password: str


class SignupForm(BaseModel):
    name: str
    email: str
    password: str
    profile_image_url: Optional[str] = "/user.png"
    id: Optional[str] = ""


class AddUserForm(SignupForm):
    role: Optional[str] = "user"

class SendCodeForm(BaseModel):
    email: str

class FaceCompareForm(BaseModel):
    sourceFacePictureBase64: str
    targetFacePictureBase64: str

class MetaInfo(BaseModel):
    bioMetaInfo: str
    deviceType: str
    ua: str
    user_id:   Optional[str] = ""


class FaceLivenessRequest(BaseModel):
    metaInfo: MetaInfo


class FaceLivenessResponse(BaseModel):
    merchant_biz_id: str
    transaction_id: str
    transaction_url: str
    face_time: datetime
    
class FaceLivenessCheckRequest(BaseModel):
    merchant_biz_id: str
    transaction_id: str
    
class FaceLivenessCheckResponse(BaseModel):
    passed: bool
    message:  Optional[str] = ""
    address: Optional[str] = ""


class SearchFormRequest(BaseModel):
    face_img: str

class AuthsTable:
    def __init__(self, db):
        self.db = db
        self.db.create_tables([Auth])

    def insert_new_auth(
        self,
        email: str,
        password: str,
        name: str,
        profile_image_url: str = "/user.png",
        role: str = "user",
        id: str = None,
        inviter_id: str = None,
        address_type: str = None,
        address: str = None,
        channel: str = None
    ) -> Optional[TypingTuple[UserModel, int]]:  # 修改返回类型声明
        
        print("insert_new_auth:1", id, role, inviter_id, address_type, address)

        auth = AuthModel(
            **{"id": id, "email": email, "password": password, "active": True}
        )
        result = Auth.create(**auth.dict())


        user = Users.insert_new_user(id, name, email, inviter_id, address_type=address_type, address=address, role=role, profile_image_url=profile_image_url, channel = channel)

        user_count = Users.get_user_count()  # 获取用户个数

        if result and user:
            return user, user_count  # 返回用户和用户个数
        else:
            return None

    # 验证用户
    def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
        # 记录日志，打印要验证的用户邮箱
        log.info(f"authenticate_user: {email}")
        try:
            # 根据邮箱和活动状态查询Auth表中的记录
            auth = Auth.get(Auth.email == email, Auth.active == True)
            # print("auth", auth)
            if auth:
                # 如果找到了匹配的Auth记录
                # 验证密码是否正确
                if verify_password(password, auth.password):
                    # 如果密码验证通过，根据Auth记录的id查询Users表中的用户信息
                    user = Users.get_user_by_id(auth.id)
                    # 返回用户信息
                    return user
                else:
                    # 如果密码验证失败，返回None
                    return None
            else:
                # 如果没有找到匹配的Auth记录��返回None
                return None
        except Exception as e:
            print("authenticate_user Exception：", e)
            # 如果发生异常，返回None
            return None

    def authenticate_user_by_api_key(self, api_key: str) -> Optional[UserModel]:
        log.info(f"authenticate_user_by_api_key: {api_key}")
        # if no api_key, return None
        if not api_key:
            return None

        try:
            user = Users.get_user_by_api_key(api_key)
            return user if user else None
        except:
            return False

    def authenticate_user_by_trusted_header(self, email: str) -> Optional[UserModel]:
        log.info(f"authenticate_user_by_trusted_header: {email}")
        try:
            auth = Auth.get(Auth.email == email, Auth.active == True)
            if auth:
                user = Users.get_user_by_id(auth.id)
                return user
        except:
            return None

    def update_user_password_by_id(self, id: str, new_password: str) -> bool:
        try:
            query = Auth.update(password=new_password).where(Auth.id == id)
            result = query.execute()

            return True if result == 1 else False
        except:
            return False

    def update_email_by_id(self, id: str, email: str) -> bool:
        try:
            query = Auth.update(email=email).where(Auth.id == id)
            result = query.execute()

            return True if result == 1 else False
        except:
            return False

    def delete_auth_by_id(self, id: str) -> bool:
        try:
            # Delete User
            result = Users.delete_user_by_id(id)

            if result:
                # Delete Auth
                query = Auth.delete().where(Auth.id == id)
                query.execute()  # Remove the rows, return number of rows removed.

                return True
            else:
                return False
        except:
            return False
        

    def update_user_id(self, old_id: str, new_id: str) -> bool:
        try:
            # 更新Auth表中的用户ID
            query = Auth.update(id=new_id).where(Auth.id == old_id)
            result = query.execute()

            # 更新Users表中的用户ID
            if result == 1:
                user_update_result = Users.update_user_id(old_id, new_id)
                return user_update_result
            else:
                return False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False



Auths = AuthsTable(DB)