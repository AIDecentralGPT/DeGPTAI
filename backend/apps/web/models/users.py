from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from peewee import *  # 导入Peewee中的所有模块
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from typing import List, Union, Optional  # 导入类型提示
import time  # 导入time模块
from datetime import datetime, timedelta

import uuid

from utils.misc import get_gravatar_url  # 导入获取Gravatar URL的方法

from apps.web.internal.db import DB, aspect_database_operations  # 导入数据库实例DB
from apps.web.models.chats import Chats  # 导入Chats模型
from apps.web.models.rewards import RewardsTableInstance
from fastapi import APIRouter, Depends, HTTPException, Request
from apps.web.models.vipstatus import VIPStatus
from apps.redis.redis_client import RedisClientInstance
import json
from apps.web.models.reward_data import RewardDateTableInstance
from apps.web.api.rewardapi import RegistAmount, InviteAmount
from apps.web.models.daily_users import DailyUsersInstance


####################
# User DB Schema
####################

# 定义Pydantic模型UserRoleUpdateProForm
class UserRoleUpdateProForm(BaseModel):
    tx: str  # 定义id字段，类型为字符串
    amount: int  # 定义role字段，类型为字符串
    vip: str # vip 类型
    viptime: str # vip 时间
    binanceflag: bool #是否币安支付

# 定义Pydantic模型UserRequest
class UserRequest(BaseModel):
    user_id: str  # 定义id字段，类型为字符串

class UserPageRequest(BaseModel):
    pageSize: int
    pageNum: int
    channel: str

# 定义User模型
class User(Model):
    id = CharField(unique=True)  # 定义唯一的字符字段id
    name = CharField()  # 定义字符字段name
    email = CharField()  # 定义字符字段email
    role = CharField()  # 定义字符字段role
    profile_image_url = TextField()  # 定义文本字段profile_image_url
    last_active_at = BigIntegerField()  # 定义大整数字段last_active_at
    updated_at = BigIntegerField()  # 定义大整数字段updated_at
    created_at = BigIntegerField()  # 定义大整数字段created_at
    api_key = CharField(null=True, unique=True)  # 定义可为空且唯一的字符字段api_key
    inviter_id = CharField(null=True)  # 邀请人id
    address_type = CharField(null=True)
    address = CharField(null=True)
    verified= CharField(null=False)
    face_id = CharField(null=True)
    merchant_biz_id= CharField(null=True)
    transaction_id= CharField(null=True)
    private_key = CharField(null=True)
    face_time = CharField(null=True)
    channel = CharField(null=True)
    models = CharField(null=True)
    language = CharField(null=True)

    class Meta:
        database = DB  # 指定数据库

# 定义Pydantic模型UserModel
class UserModel(BaseModel):
    id: str  # 定义id字段，类型为字符串
    name: str  # 定义name字段，类型为字符串
    email: str  # 定义email字段，类型为字符串
    role: str = "user"  # 定义role字段，类型为字符串，默认值为"pending"
    profile_image_url: str  # 定义profile_image_url字段，类型为字符串

    last_active_at: int  # 定义last_active_at字段，类型为整型，表示epoch时间戳
    updated_at: int  # 定义updated_at字段，类型为整型，表示epoch时间戳
    created_at: int  # 定义created_at字段，类型为整型，表示epoch时间戳

    api_key: Optional[str] = None  # 定义可选的api_key字段，类型为字符串，默认值为None
    inviter_id: Optional[str] = None
    address_type: Optional[str] = None
    verified: Optional[bool] = False
    face_id: Optional[str] = None
    merchant_biz_id: Optional[str] = None
    transaction_id: Optional[str] = None
    private_key: Optional[str] = None
    face_time: Optional[datetime] = None
    address: Optional[str] = None
    channel: Optional[str] = None
    models: Optional[str] = None
    language: Optional[str] = None

# 定义Pydantic近15天统计数据模型UserLatelyModel
class UserLatelyModel(BaseModel):
    wallet_count: Optional[int] = 0
    channel_count: Optional[int] = 0
    kyc_count: Optional[int] = 0
    create_date: Optional[str] = None

# 定义Pydantic模型UserModel
class ChannelTotalModel(BaseModel):
    channel: str  # 第三方标识
    total: int  # 总数

# 定义Pydantic模型UserTotalModel
class UserTotalModel(BaseModel):
    total: int = 0  # 总数
    wallet_total: int = 0  # 钱包总数
    channel_total: int = 0  # 第三方注册总数
    vip_total: int = 0  # VIP总数
    active_today: int = 0  # 活跃用户总数
    kyc_total: int = 0  # 访客总数

# 定义Pydantic模型UserTotalModel
class UserDisperModel(BaseModel):
    date_list: List[str] = []  # 日期
    wallet_list: List[int] = []  # 钱包注册数
    channel_list: List[int] = []  # 第三方注册数
    kyc_list: List[int] = []  # kyc认证数
    
####################
# Forms
####################

# 定义Pydantic模型UserRoleUpdateForm
class UserRoleUpdateForm(BaseModel):
    id: str  # 定义id字段，类型为字符串
    role: str  # 定义role字段，类型为字符串

# 定义Pydantic模型UserUpdateForm
class UserUpdateForm(BaseModel):
    name: str  # 定义name字段，类型为字符串
    email: str  # 定义email字段，类型为字符串
    profile_image_url: str  # 定义profile_image_url字段，类型为字符串
    password: Optional[str] = None  # 定义可选的password字段，类型为字符串，默认值为None

# 更新用户选择模型
class UserModelsUpdateForm(BaseModel):
    models: str  # 定义模型字段，类型为字符串

# 更新用户选择语言
class UserLanguageUpdateForm(BaseModel):
    language: str  # 定义language字段，类型为字符串

# 定义UsersTable类，用于操作User表
class UsersTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([User])  # 创建User表

    # 判断 result 是否是以0x开头的钱包地址
    def is_ethereum_address(address):
        print("验证是不是钱包地址" ,isinstance(address, str) , address.startswith("0x"))
        return isinstance(address, str) and address.startswith("0x")

    # 插入新用户
    def insert_new_user(
        self,
        id: str,
        name: str,
        email: str,
        inviter_id: str ,
        profile_image_url: str = "/user.png",
        role: str = "user",
        address_type: str = None,
        verified: bool = False,
        face_id: str = None,
        merchant_biz_id: str = None,
        transaction_id: str = None,
        private_key: str = None,
        address: str = None,
        channel: str = None
    ) -> Optional[UserModel]:
        
        # 创建UserModel实例
        user = UserModel(
            **{
                "id": id,
                "name": name,
                "email": email,
                "role": role,
                "profile_image_url": profile_image_url,
                "last_active_at": int(time.time()),
                "created_at": int(time.time()),
                "updated_at": int(time.time()),
                "inviter_id": inviter_id,
                "address_type": address_type,
                "address": address,
                "verified":  verified,
                "face_id": face_id,
                "merchant_biz_id": merchant_biz_id,
                "transaction_id": transaction_id,
                "private_key": private_key,
                "channel": channel
            }
        )

        print("User.create address", user.address)

        # 在数据库中创建新用户
        result = User.create(**user.model_dump())
        # 创建用户更新一个活跃数
        DailyUsersInstance.refresh_active_today(900000000)
        Users.update_user_last_active_by_id(result.id)

        print("User.create result", result.id)

        rewarddate = RewardDateTableInstance.get_current_open()
        if rewarddate is not None:
            # 获取当前日期
            current_date = datetime.now().date()
            if rewarddate.start_time.date() <= current_date <= rewarddate.end_time.date():
                # 在这里给新钱包发送奖励
                if result and UsersTable.is_ethereum_address(result.id):
                    print("============创建注册奖励1============")
                    # 添加邀请建立
                    if user.inviter_id is not None and user.inviter_id != '':
                        # 获取邀请人信息
                        invite_user_ret = User.get_or_none(User.id == inviter_id)
                        # 邀请人存在创建注册奖励和邀请奖励
                        if invite_user_ret is not None:
                            # 生成关联字符串
                            invitee = str(uuid.uuid4())
                            invite_list = RewardsTableInstance.get_invitee_today_history(inviter_id)   
                            # 校验邀请人是否KYC认证
                            invite_user_dict = model_to_dict(invite_user_ret)
                            invite_user = UserModel(**invite_user_dict)
                            if invite_user.verified:
                                # 注册奖励绑定邀请人
                                RewardsTableInstance.create_reward(user.id, RegistAmount, "new_wallet",True, invitee)
                                if len(invite_list) < 20:
                                    print("邀请人得奖励", user.inviter_id)
                                    RewardsTableInstance.create_reward(user.inviter_id, InviteAmount, "invite", True, invitee)
                            else:
                                # 注册奖励绑定邀请人
                                RewardsTableInstance.create_reward(user.id, RegistAmount, "new_wallet",True, invitee)
                                if len(invite_list) < 20:
                                    print("邀请人得奖励0", user.inviter_id)
                                    RewardsTableInstance.create_reward(user.inviter_id, 0, "invite", False, invitee)
                    else:
                        # 注册奖励
                        RewardsTableInstance.create_reward(user.id, RegistAmount, "new_wallet",True)
        
        # return user info:
        return user  # 返回创建的用户 

    # 根据id获取用户
    @aspect_database_operations
    def get_user_by_id(self, id: str) -> Optional[UserModel]:
        try:
            # 从Redis获取用户信息
            user_dict = RedisClientInstance.get_value_by_key(f"user:{id}")
            if user_dict is None:
                user = User.get_or_none(User.id == id)  # 查询数据库中的用户
                if user is None:
                    return None
                else:
                    user_dict = model_to_dict(user)  # 将数据库对象转换为字典
                    RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                    user_model = UserModel(**user_dict)  # 将字典转换为Pydantic模型  
                    return user_model
            else:
                user_model = UserModel(**user_dict)
                print("获取完毕用户")
                # print("用户模型：", user_model)
                return user_model
        except Exception as e:
            print(f"get_user_by_id补货错误: {e}")
            return None  # 如果查询失败，返回None        

    # 获取邀请的所有用户
    def get_users_invited(self, inviter_id: str) -> List[UserModel]:
        try:
            print("开始根据inviter_id获取所有用户")
            users = User.select().where(User.inviter_id == inviter_id)  # 查询数据库中的用户
            user_list = [UserModel(**model_to_dict(user)) for user in users]  # 将数据库对象转换为字典并转换为Pydantic模型
            print("获取到的用户模型列表：", user_list)
            return user_list
        except Exception as e:
            print(f"get_users_invited捕获错误: {e}")
            return []  # 如果查询失败，返回空列表

    # 根据api_key获取用户
    def get_user_by_api_key(self, api_key: str) -> Optional[UserModel]:
        try:
            user = User.get(User.api_key == api_key)  # 查询数据库中的用户
            return UserModel(**model_to_dict(user))  # 将数据库对象转换为Pydantic模型并返回
        except:
            return None  # 如果查询失败，返回None

    # 根据email获取用户
    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        try:
            user = User.get(User.email == email)  # 查询数据库中的用户
            return UserModel(**model_to_dict(user))  # 将数据库对象转换为Pydantic模型并返回
        except:
            return None  # 如果查询失败，返回None

    # 获取用户列表
    def get_users(self, skip: int = 0, limit: int = 50, role: str = "", search: str = "", verified: str = "", channel: str = "") -> List[UserModel]:
        query = User.select()
        # 角色筛选
        if role:
            query = query.where(User.role == role)
        # 搜索
        if search:
            query = query.where((User.name.contains(search)) | (User.id.contains(search)))
        # KYC认证筛选
        if verified:
            query = query.where(User.verified == verified)

        # 渠道筛选
        if channel:
            query = query.where(User.channel == channel)

        # 获取总记录数
        total = query.count()

        # 获取当前页的记录
        users = [
            UserModel(**model_to_dict(user))
            for user in query.limit(10).offset((skip - 1)*10)  # 限制查询结果的数量和偏移量
        ]

        # 返回结果
        return {'total': total, 'users': users}

    # 获取用户数量
    def get_num_users(self) -> Optional[int]:
        return User.select().count()  # 查询用户数量

    # 获取第一个用户
    def get_first_user(self) -> UserModel:
        try:
            user = User.select().order_by(User.created_at).first()  # 查询第一个用户
            return UserModel(**model_to_dict(user))  # 将数据库对象转换为Pydantic模型并返回
        except:
            return None  # 如果查询失败，返回None

    # 根据id更新用户角色
    def update_user_role_by_id(self, id: str, role: str) -> Optional[UserModel]:
        try:
            query = User.update(role=role).where(User.id == id)  # 更新用户角色
            query.execute()  # 执行更新操作
            user = User.get(User.id == id)  # 查询更新后的用户
            user_dict = model_to_dict(user)  # 将数据库对象转换为字典
            RedisClientInstance.add_key_value(f"user:{id}", user_dict)
            return UserModel(**user_dict)  # 将数据库对象转换为Pydantic模型并返回
        except:
            return None  # 如果更新失败，返回None

    # 根据id更新用户的profile_image_url
    def update_user_profile_image_url_by_id(
        self, id: str, profile_image_url: str
    ) -> Optional[UserModel]:
        try:
            query = User.update(profile_image_url=profile_image_url).where(
                User.id == id
            )  # 更新用户的profile_image_url
            query.execute()  # 执行更新操作

            user = User.get(User.id == id)  # 查询更新后的用户
            user_dict = model_to_dict(user)  # 将数据库对象转换为字典
            RedisClientInstance.add_key_value(f"user:{id}", user_dict)
            return UserModel(**user_dict)  # 将数据库对象转换为Pydantic模型并返回
        except:
            return None  # 如果更新失败，返回None

    # 根据id更新用户的last_active_at
    @aspect_database_operations
    def update_user_last_active_by_id(self, id: str) -> Optional[UserModel]:
        try:
            # print("update_user_last_active_by_id")
            query = User.update(last_active_at=int(time.time())).where(User.id == id)  # 更新用户的last_active_at
            query.execute()  # 执行更新操作
            # print("update_user_last_active_by_id222222")

            user = User.get(User.id == id)  # 查询更新后的用户
            user_dict = model_to_dict(user)
            RedisClientInstance.add_key_value(f"user:{id}", user_dict)
            # print("update_user_last_active_by_id33333", user)
            # print(4444, UserModel(**model_to_dict(user)))
            return UserModel(**model_to_dict(user))  # 将数据库对象转换为Pydantic模型并返回
        except Exception as e:
            print("update_user_last_active_by_id error", e)
            return None  # 如果更新失败，返回None

    # 根据id更新用户信息
    def update_user_by_id(self, id: str, updated: dict) -> Optional[UserModel]:
        try:
            query = User.update(**updated).where(User.id == id)  # 更新用户信息
            query.execute()  # 执行更新操作

            user = User.get(User.id == id)  # 查询更新后的用户
            return UserModel(**model_to_dict(user))  # 将数据库对象转换为Pydantic模型并返回
        except:
            return None  # 如果更新失败，返回None

    # 根据id删除用户
    def delete_user_by_id(self, id: str) -> bool:
        try:
            # 删除用户的聊天记录
            result = Chats.delete_chats_by_user_id(id)  # 调用Chats模型的删除方法
            if result:
                # 删除用户
                query = User.delete().where(User.id == id)  # 删除用户记录
                query.execute()  # 执行删除操作
                RedisClientInstance.delete_key(f"user:{id}")
                return True  # 如果删除成功，返回True
            else:
                return False  # 如果删除失败，返回False
        except:
            return False  # 如果出现异常，返回False

    # 根据id更新用户的api_key
    def update_user_api_key_by_id(self, id: str, api_key: str) -> str:
        try:
            query = User.update(api_key=api_key).where(User.id == id)  # 更新用户的api_key
            result = query.execute()  # 执行更新操作

            return True if result == 1 else False  # 如果更新成功，返回True，否则返回False
        except:
            return False  # 如果出现异常，返回False

    # 根据id获取用户的api_key
    def get_user_api_key_by_id(self, id: str) -> Optional[str]:
        try:
            user = User.get(User.id == id)  # 查询用户
            return user.api_key  # 返回用户的api_key
        except:
            return None  # 如果查询失败，返回None
        
    # 根据face_id获取user_id
    def get_user_id_by_face_id(self, face_id: str) -> Optional[UserModel]:
        try:
            user = User.get(User.face_id == face_id)  # 查询用户
            return user # 返回用户
        except:
            return None  # 如果查询失败，返回None
        

    def update_user_id(old_id: str, new_id: str) -> bool:
        try:
            query = UserModel.update(id=new_id).where(UserModel.id == old_id)
            result = query.execute()
            return True if result == 1 else False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
             
    # 更新用户的transaction_id和merchant_biz_id
    def update_user_verify_info(self, id: str, transaction_id: str, merchant_biz_id: str, face_time: datetime) -> bool:
        try:
            query = User.update(transaction_id=transaction_id, merchant_biz_id =merchant_biz_id, face_time = face_time).where(User.id == id)
            result = query.execute()
            if result == 1:
                user = User.get(User.id == id)  # 查询更新后的用户
                user_dict = model_to_dict(user)  # 将数据库对象转换为字典
                RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                return True
            else:
                return False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
  
    # 更新用户是否完成活体检测认证
    def update_user_verified(self, id: str, verified: bool, face_id: str) -> bool:
        try:
            query = User.update(verified=verified, face_id =face_id).where(User.id == id)
            result = query.execute()
            if result == 1:
                user = User.get(User.id == id)  # 查询更新后的用户
                user_dict = model_to_dict(user)  # 将数据库对象转换为字典
                RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                return True
            else:
                return False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
        
    # 更新用户选择模型
    def update_user_models(self, id: str, models: str) -> bool:
        try:
            query = User.update(models=models).where(User.id == id)
            result = query.execute()
            if result == 1:
                user = User.get(User.id == id)  # 查询更新后的用户
                user_dict = model_to_dict(user)  # 将数据库对象转换为字典
                RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                return True
            else:
                return False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
        
    # 更新用户选择语言
    def update_user_language(self, id: str, language: str) -> bool:
        try:
            query = User.update(language=language).where(User.id == id)
            result = query.execute()
            if result == 1:
                user = User.get(User.id == id)  # 查询更新后的用户
                user_dict = model_to_dict(user)  # 将数据库对象转换为字典
                RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                return True
            else:
                return False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
        
    def get_user_count(self) -> int:
        return User.select().count()  # 查询用户数量
    
    def get_third_total(self, channel: Optional[str]="") -> int:
        if channel == "":
            return User.select(User.channel, fn.Count(User.id).alias('total')).where(User.channel is not None, User.channel != '', User.id.like('0x%')).count();
        else:
            return User.select(User.channel, fn.Count(User.id).alias('total')).where(User.channel == channel, User.id.like('0x%')).count();

    def get_third_group_total(self) -> Optional[ChannelTotalModel]:
        return User.select(User.channel, fn.Count(User.id).alias('total')).where(User.channel is not None, User.channel != '', User.id.like('0x%')).group_by(User.channel);

    def get_user_total(self) -> Optional[UserTotalModel]:
        total = User.select().count()
        wallet_total = User.select().where(User.role != 'visitor').count()
        channel_total = User.select().where(User.channel is not None, User.channel != '', User.id.like('0x%')).count()
        vip_total = User.select().where(User.id << (VIPStatus.select(VIPStatus.user_id))).count()
        kyc_total = User.select().where(User.verified == 't').count()

        active_today = DailyUsersInstance.today_active_users()
        # datelist = [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.65, 
        #             0.76, 0.82, 0.865, 0.888, 0.99, 0.993, 0.996, 1, 1, 1, 1, 1, 1]
        # current_hour = datetime.now().hour
        # active_today_cal = int(active_today * datelist[current_hour])
        data = {
            "total": total,
            "wallet_total": wallet_total,
            "channel_total": channel_total,
            "vip_total": vip_total,
            "active_today": active_today,
            "kyc_total": kyc_total
        }
        return UserTotalModel(**data)
    
    def get_regist_total(self) -> int:
        return User.select().where(User.id.like('0x%')).count()
    
    def get_regist_reward_total(self) -> int:
        return User.select().where(User.verified == True).count()

    def get_user_lately(self) -> Optional[List[UserLatelyModel]]:
        # 查询数据库中的用户
        now = datetime.now()
        fifteen_days_ago = now - timedelta(days=15)
        target_timestamp = int(fifteen_days_ago.timestamp())
        sql = f"select sum(case when role = 'visitor' then 0 else 1 end) as wallet_count, \
            sum(case when channel is not NULL and channel != '' then 1 else 0 end) as channel_count, \
            sum(case when verified = 't' then 1 else 0 end) as kyc_count, \
            to_char(to_timestamp(created_at) AT TIME ZONE 'Asia/Shanghai', 'MM-DD') AS create_date from \"user\" \
            where created_at > {target_timestamp} group by to_char(to_timestamp(created_at) AT TIME ZONE 'Asia/Shanghai', 'MM-DD')"
        users = User.raw(sql).dicts()
        # 将数据库对象转换为字典并转换为Pydantic模型
        user_list = [UserLatelyModel(**user) for user in users]
        return user_list

    def get_third_list(self, pageNum: Optional[int]=1, pageSize: Optional[int]=10, channel: Optional[str]="") -> Optional[UserModel]:
        try:
            if channel == "":
                users = User.select().where(User.channel is not None, User.channel != '', User.id.like('0x%')).order_by(User.created_at.desc()).paginate(pageNum, pageSize);
                return [UserModel(**model_to_dict(user)) for user in users]
            else:
                users = User.select().where(User.channel == channel, User.id.like('0x%')).order_by(User.created_at.desc()).paginate(pageNum, pageSize);
                return [UserModel(**model_to_dict(user)) for user in users]
        except Exception as e:
            print(f"get_third_list Exception: {e}")
            return None

# 实例化UsersTable类
Users = UsersTable(DB)
