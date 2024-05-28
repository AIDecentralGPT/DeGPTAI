from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from peewee import *  # 导入Peewee中的所有模块
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from typing import List, Union, Optional  # 导入类型提示
import time  # 导入time模块
from utils.misc import get_gravatar_url  # 导入获取Gravatar URL的方法

from apps.web.internal.db import DB  # 导入数据库实例DB
from apps.web.models.chats import Chats  # 导入Chats模型

####################
# User DB Schema
####################

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

# 定义UsersTable类，用于操作User表
class UsersTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([User])  # 创建User表

    # 插入新用户
    def insert_new_user(
        self,
        id: str,
        name: str,
        email: str,
        profile_image_url: str = "/user.png",
        role: str = "user",
    ) -> Optional[UserModel]:
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
            }
        )  # 创建UserModel实例
        result = User.create(**user.model_dump())  # 在数据库中创建新用户
        if result:
            return user  # 返回创建的用户
        else:
            return None  # 如果创建失败，返回None

    # 根据id获取用户
    def get_user_by_id(self, id: str) -> Optional[UserModel]:
        try:
            user = User.get(User.id == id)  # 查询数据库中的用户
            return UserModel(**model_to_dict(user))  # 将数据库对象转换为Pydantic模型并返回
        except:
            return None  # 如果查询失败，返回None

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
    def get_users(self, skip: int = 0, limit: int = 50) -> List[UserModel]:
        return [
            UserModel(**model_to_dict(user))
            for user in User.select()
            # .limit(limit).offset(skip)  # 限制查询结果的数量和偏移量
        ]

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
            return UserModel(**model_to_dict(user))  # 将数据库对象转换为Pydantic模型并返回
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
            return UserModel(**model_to_dict(user))  # 将数据库对象转换为Pydantic模型并返回
        except:
            return None  # 如果更新失败，返回None

    # 根据id更新用户的last_active_at
    def update_user_last_active_by_id(self, id: str) -> Optional[UserModel]:
        try:
            query = User.update(last_active_at=int(time.time())).where(User.id == id)  # 更新用户的last_active_at
            query.execute()  # 执行更新操作

            user = User.get(User.id == id)  # 查询更新后的用户
            return UserModel(**model_to_dict(user))  # 将数据库对象转换为Pydantic模型并返回
        except:
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

# 实例化UsersTable类
Users = UsersTable(DB)
