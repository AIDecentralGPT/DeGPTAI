from pydantic import BaseModel
from peewee import *
from playhouse.shortcuts import model_to_dict
from typing import List, Union, Optional
import time
from datetime import datetime, timedelta

import uuid

from utils.misc import get_gravatar_url

from apps.web.internal.db import DB, aspect_database_operations
from apps.web.models.chats import Chats
from apps.web.models.rewards import RewardsTableInstance
from fastapi import APIRouter, Depends, HTTPException, Request
from apps.web.models.vip import VIPStatus
from apps.redis.redis_client import RedisClientInstance
import json


####################
# User DB Schema
####################

# Define the Pydantic model UserRoleEtuProForm
class UserRoleUpdateProForm(BaseModel):
    tx: str  # Define the ID field as a string type
    amount: int  # Define the role field as a string type

# Define Pydance Model UserRequest
class UserRequest(BaseModel):
    user_id: str  # Define the ID field as a string type

class UserPageRequest(BaseModel):
    pageSize: int
    pageNum: int
    channel: str

# Define User Model
class User(Model):
    id = CharField(unique=True)  # Define a unique character field ID
    name = CharField()  # Define character field name
    email = CharField()  # Define character field email
    role = CharField()  # Define character field role
    profile_image_url = TextField()  # Define the text field profile_image_url
    last_active_at = BigIntegerField()  # Define the large integer field last_mactive_at
    updated_at = BigIntegerField()  # Define the large integer field updated_at
    created_at = BigIntegerField()  # Define the large integer field created_at
    api_key = CharField(null=True, unique=True)  # Define a unique and empty character field api_key
    inviter_id = CharField(null=True)  # Inviter ID
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
        database = DB  # Specify Database

# Define Pydance Model UserModel
class UserModel(BaseModel):
    id: str  # Define a unique character field ID
    name: str  # Define character field name
    email: str  # Define character field email
    role: str = "user"  # Define character field role
    profile_image_url: str  # Define the text field profile_image_url

    last_active_at: int  # Define the large integer field last_mactive_at
    updated_at: int  # Define the large integer field updated_at
    created_at: int  # Define the large integer field created_at

    api_key: Optional[str] = None  # Define optional api_key field, type string, default value None
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

# Define Pydance's recent 15 day statistical data model UserLatelyModel
class UserLatelyModel(BaseModel):
    wallet_count: Optional[int] = 0
    channel_count: Optional[int] = 0
    kyc_count: Optional[int] = 0
    create_date: Optional[str] = None

# Define Pydance Model UserModel
class ChannelTotalModel(BaseModel):
    channel: str  # Third party identification
    total: int  # total

# Define Pydance model UserTotalModel
class UserTotalModel(BaseModel):
    total: int = 0  # total
    wallet_total: int = 0  # Total number of wallets
    channel_total: int = 0  # Total number of third-party registrations
    vip_total: int = 0  # Total number of VIPs
    kyc_total: int = 0  # Total number of visitors

# Define the Pydance model UserDisperModel
class UserDisperModel(BaseModel):
    date_list: List[str] = []  # date collection
    wallet_list: List[int] = []  # wallet collection
    channel_list: List[int] = []  # channel collection
    kyc_list: List[int] = []  # KYC authentication collection
    
####################
# Forms
####################

# Define Pydantic Model UserRoleUpdate Form
class UserRoleUpdateForm(BaseModel):
    id: str  # Define the ID field as a string type
    role: str  # Define the role field as a string type

# Define Pydance Model UserUpdating Form
class UserUpdateForm(BaseModel):
    name: str  # Define the name field as a string type
    email: str  # Define the email field as a string type
    profile_image_url: str  # Define the profile_image_url field as a string type
    password: Optional[str] = None  # Define an optional password field, of type string, with a default value of None

# Update user selection model
class UserModelsUpdateForm(BaseModel):
    models: str  # Define model fields of type string

# Update user selection language
class UserLanguageUpdateForm(BaseModel):
    language: str  # Define the language field as a string type

# Define the UsersTable class for manipulating the User table
class UsersTable:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        self.db.create_tables([User])  # Create User Table

    # Determine if the result is a wallet address starting with 0x
    def is_ethereum_address(address):
        print("Verify if it is a wallet address:" ,isinstance(address, str) , address.startswith("0x"))
        return isinstance(address, str) and address.startswith("0x")

    # Insert new user
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
        
        # Create UserModel instance
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

        # Create a new user in the database
        result = User.create(**user.model_dump())

        print("User.create result", result.id)

        # Send rewards to the new wallet here
        # if result and UsersTable.is_ethereum_address(result.id):
        #     print("============Create registration reward============")
        #     # Add invitation to create
        #     if user.inviter_id is not None and user.inviter_id != '':
        #         # Obtain inviter information
        #         invite_user_ret = User.get_or_none(User.id == inviter_id)
        #         # The inviter has created registration rewards and invitation rewards
        #         if invite_user_ret is not None:
        #             # Generate associated strings
        #             invitee = str(uuid.uuid4())
        #             invite_list = RewardsTableInstance.get_invitee_today_history(inviter_id)   
        #             # Verify whether the inviter has KYC authentication
        #             invite_user_dict = model_to_dict(invite_user_ret)
        #             invite_user = UserModel(**invite_user_dict)
        #             if invite_user.verified:
        #                 # Register reward binding inviter
        #                 RewardsTableInstance.create_reward(user.id, 1000, "new_wallet",True, invitee)
        #                 if len(invite_list) < 24:
        #                     print("Inviters receive rewards:", user.inviter_id)
        #                     RewardsTableInstance.create_reward(user.inviter_id, 6000, "invite", True, invitee)
        #             else:
        #                 # Register reward binding inviter
        #                 RewardsTableInstance.create_reward(user.id, 1000, "new_wallet",True, invitee)
        #                 if len(invite_list) < 24:
        #                     print("Inviters receive rewards:", user.inviter_id)
        #                     RewardsTableInstance.create_reward(user.inviter_id, 0, "invite", False, invitee)
        #     else:
        #         # Registration Rewards
        #         RewardsTableInstance.create_reward(user.id, 1000, "new_wallet",True)
        
        # return user info:
        return user  # Return the created user 

    # Retrieve users based on their ID
    @aspect_database_operations
    def get_user_by_id(self, id: str) -> Optional[UserModel]:
        try:
            # Retrieve user information from Redis
            user_dict = RedisClientInstance.get_value_by_key(f"user:{id}")
            if user_dict is None:
                user = User.get_or_none(User.id == id)  # Query users in the database
                if user is None:
                    return None
                else:
                    user_dict = model_to_dict(user)  # Convert database objects to dictionaries
                    RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                    user_model = UserModel(**user_dict)  # Convert dictionary to Pydantic model
                    return user_model
            else:
                user_model = UserModel(**user_dict)
                return user_model
        except Exception as e:
            print(f"get_user_by_id error: {e}")
            # If the query fails, return None
            return None

    # Get all invited users
    def get_users_invited(self, inviter_id: str) -> List[UserModel]:
        try:
            # Query users in the database
            users = User.select().where(User.inviter_id == inviter_id)
            # Convert database objects into dictionaries and Pydantic models
            user_list = [UserModel(**model_to_dict(user)) for user in users]
            print("Obtained user model list：", user_list)
            return user_list
        except Exception as e:
            print(f"get_users_invited error: {e}")
            return []  # If the query fails, return an empty list

    # Retrieve users based on api_key
    def get_user_by_api_key(self, api_key: str) -> Optional[UserModel]:
        try:
            # Query users in the database
            user = User.get(User.api_key == api_key)
            # Convert database objects to Pydantic models and return
            return UserModel(**model_to_dict(user))
        except:
            # If the query fails, return None
            return None

    # Retrieve users based on email
    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        try:
            # Query users in the database
            user = User.get(User.email == email)
            # Convert database objects to Pydantic models and return
            return UserModel(**model_to_dict(user))
        except:
            # If the query fails, return None
            return None

    # Get user list
    def get_users(self, skip: int = 0, limit: int = 50, role: str = "", search: str = "", verified: str = "", channel: str = "") -> List[UserModel]:
        query = User.select()
        # Role screening
        if role:
            query = query.where(User.role == role)
        # search
        if search:
            query = query.where((User.name.contains(search)) | (User.id.contains(search)))
        # KYC authentication screening
        if verified:
            query = query.where(User.verified == verified)

        # Channel screening
        if channel:
            query = query.where(User.channel == channel)

        # Obtain the total number of records
        total = query.count()

        # Retrieve the records of the current page
        users = [
            UserModel(**model_to_dict(user))
            for user in query.limit(10).offset((skip - 1)*10) # Limit the number and offset of query results
        ]

        # Return result
        return {'total': total, 'users': users}

    # Obtain the number of users
    def get_num_users(self) -> Optional[int]:
        return User.select().count()

    # Get the first user
    def get_first_user(self) -> UserModel:
        try:
            user = User.select().order_by(User.created_at).first()  # Search for the first user
            return UserModel(**model_to_dict(user))  # Convert database objects to Pydantic models and return
        except:
            # If the query fails, return None
            return None

    # Update user roles based on ID
    def update_user_role_by_id(self, id: str, role: str) -> Optional[UserModel]:
        try:
            query = User.update(role=role).where(User.id == id)  # Update user roles
            query.execute()  # Perform update operation
            user = User.get(User.id == id)  # Query updated users
            user_dict = model_to_dict(user)  # Convert database objects to dictionaries
            RedisClientInstance.add_key_value(f"user:{id}", user_dict)
            return UserModel(**user_dict)  # Convert database objects to Pydantic models and return
        except:
            # If the update fails, return None
            return None

    # Update the user's profile_image_url based on their ID
    def update_user_profile_image_url_by_id(
        self, id: str, profile_image_url: str
    ) -> Optional[UserModel]:
        try:
            query = User.update(profile_image_url=profile_image_url).where(
                User.id == id
            )  # Update user's profile_image_url
            query.execute()  # Perform update operation

            user = User.get(User.id == id)  # Query updated users
            user_dict = model_to_dict(user)  # Convert database objects to dictionaries
            RedisClientInstance.add_key_value(f"user:{id}", user_dict)
            return UserModel(**user_dict)  # Convert database objects to Pydantic models and return
        except:
            # If the update fails, return None
            return None

    # Update the user's last_mactive_at based on their ID
    @aspect_database_operations
    def update_user_last_active_by_id(self, id: str) -> Optional[UserModel]:
        try:
            print("update_user_last_active_by_id")
            query = User.update(last_active_at=int(time.time())).where(User.id == id)  # Update user's last_mactive_at
            query.execute()  # Perform update operation
            user = User.get(User.id == id)  # Query updated users
            return UserModel(**model_to_dict(user))  # Convert database objects to Pydantic models and return
        except Exception as e:
            print("update_user_last_active_by_id error", e)
            # If the update fails, return None
            return None

    # Update user information based on ID
    def update_user_by_id(self, id: str, updated: dict) -> Optional[UserModel]:
        try:
            query = User.update(**updated).where(User.id == id)  # Update user information
            query.execute()  # Perform update operation

            user = User.get(User.id == id)  # Query updated users
            return UserModel(**model_to_dict(user))  # Convert database objects to Pydantic models and return
        except:
            # If the update fails, return None
            return None

    # Delete users based on their ID
    def delete_user_by_id(self, id: str) -> bool:
        try:
            # Delete user's chat history
            result = Chats.delete_chats_by_user_id(id)  # Call the deletion method of Chats model
            if result:
                # delete user
                query = User.delete().where(User.id == id)  # Delete user records
                query.execute()  # Perform deletion operation
                RedisClientInstance.delete_key(f"user:{id}")
                return True  # If the deletion is successful, return True
            else:
                return False  # If deletion fails, return False
        except:
            return False  # If an exception occurs, return False

    # Update the user's api_key based on their ID
    def update_user_api_key_by_id(self, id: str, api_key: str) -> str:
        try:
            query = User.update(api_key=api_key).where(User.id == id)  # Update the user's api_key
            result = query.execute()  # Perform update operation

            return True if result == 1 else False  # If the update is successful, return True; otherwise, return False
        except:
            return False  # If an exception occurs, return False

    # Retrieve the user's api_key based on their ID
    def get_user_api_key_by_id(self, id: str) -> Optional[str]:
        try:
            user = User.get(User.id == id)  # Query users
            return user.api_key  # Return the user's api_key
        except:
            return None  # If the query fails, return None
        
    # Obtain user_id based on face_id
    def get_user_id_by_face_id(self, face_id: str) -> Optional[UserModel]:
        try:
            user = User.get(User.face_id == face_id)  # Query users
            return user # Return to User
        except:
            return None  # If the query fails, return None
        

    def update_user_id(old_id: str, new_id: str) -> bool:
        try:
            query = UserModel.update(id=new_id).where(UserModel.id == old_id)
            result = query.execute()
            return True if result == 1 else False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
             
    # Update the user's transaction-id and merchant_biz_id
    def update_user_verify_info(self, id: str, transaction_id: str, merchant_biz_id: str, face_time: datetime) -> bool:
        try:
            query = User.update(transaction_id=transaction_id, merchant_biz_id =merchant_biz_id, face_time = face_time).where(User.id == id)
            result = query.execute()
            if result == 1:
                user = User.get(User.id == id)  # Query updated users
                user_dict = model_to_dict(user)  # Convert database objects to dictionaries
                RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                return True
            else:
                return False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
  
    # Update whether the user has completed live detection authentication
    def update_user_verified(self, id: str, verified: bool, face_id: str) -> bool:
        try:
            query = User.update(verified=verified, face_id =face_id).where(User.id == id)
            result = query.execute()
            if result == 1:
                user = User.get(User.id == id)  # Query updated users
                user_dict = model_to_dict(user)  # Convert database objects to dictionaries
                RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                return True
            else:
                return False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
        
    # Update user selection model
    def update_user_models(self, id: str, models: str) -> bool:
        try:
            query = User.update(models=models).where(User.id == id)
            result = query.execute()
            if result == 1:
                user = User.get(User.id == id)  # Query updated users
                user_dict = model_to_dict(user)  # Convert database objects to dictionaries
                RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                return True
            else:
                return False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
        
    # Update user selection language
    def update_user_language(self, id: str, language: str) -> bool:
        try:
            query = User.update(language=language).where(User.id == id)
            result = query.execute()
            if result == 1:
                user = User.get(User.id == id)  # Query updated users
                user_dict = model_to_dict(user)  # Convert database objects to dictionaries
                RedisClientInstance.add_key_value(f"user:{id}", user_dict)
                return True
            else:
                return False
        except Exception as e:
            print(f"update_user_id Exception: {e}")
            return False
        
    def get_user_count(self) -> int:
        return User.select().count()  # Query the number of users
    
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
        data = {    
            "total": total,
            "wallet_total": wallet_total,
            "channel_total": channel_total,
            "vip_total": vip_total,
            "kyc_total": kyc_total
        }
        return UserTotalModel(**data)
    
    def get_regist_total(self) -> int:
        return User.select().where(User.id.like('0x%')).count()
    
    def get_regist_reward_total(self) -> int:
        return User.select().where(User.verified == True).count()

    def get_user_lately(self) -> Optional[List[UserLatelyModel]]:
        # Query users in the database
        now = datetime.now()
        fifteen_days_ago = now - timedelta(days=15)
        target_timestamp = int(fifteen_days_ago.timestamp())
        sql = f"select sum(case when role = 'visitor' then 0 else 1 end) as wallet_count, \
            sum(case when channel is not NULL and channel != '' then 1 else 0 end) as channel_count, \
            sum(case when verified = 't' then 1 else 0 end) as kyc_count, \
            to_char(to_timestamp(created_at) AT TIME ZONE 'Asia/Shanghai', 'MM-DD') AS create_date from \"user\" \
            where created_at > {target_timestamp} group by to_char(to_timestamp(created_at) AT TIME ZONE 'Asia/Shanghai', 'MM-DD')"
        users = User.raw(sql).dicts()
        # Convert database objects into dictionaries and Pydantic models
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

# Instantiate UsersTable class
Users = UsersTable(DB)
