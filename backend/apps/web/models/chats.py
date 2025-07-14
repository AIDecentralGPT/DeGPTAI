from pydantic import BaseModel
from typing import List, Union, Optional
from peewee import *
from playhouse.shortcuts import model_to_dict

import json
import uuid
import time

from apps.web.internal.db import DB, aspect_database_operations
from apps.redis.redis_client import RedisClientInstance

####################
# Chat DB Schema
####################


class Chat(Model):
    id = CharField(unique=True)
    user_id = CharField()
    title = TextField()
    chat = TextField()  # Save Chat JSON as Text

    created_at = BigIntegerField()
    updated_at = BigIntegerField()

    share_id = CharField(null=True, unique=True)
    archived = BooleanField(default=False)

    class Meta:
        database = DB


class ChatModel(BaseModel):
    id: str
    user_id: str
    title: str
    chat: Optional[str] = None

    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch
    

    share_id: Optional[str] = None
    archived: bool = False


####################
# Forms
####################


class ChatForm(BaseModel):
    chat: dict


class ChatTitleForm(BaseModel):
    title: str


class ChatResponse(BaseModel):
    id: str
    user_id: str
    title: str
    chat: dict
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch
    share_id: Optional[str] = None  # id of the chat to be shared
    archived: bool


class ChatTitleIdResponse(BaseModel):
    id: str
    title: str
    updated_at: int
    created_at: int


class ChatTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([Chat])

    def insert_new_chat(self, user_id: str, form_data: ChatForm) -> Optional[ChatModel]:
        # 生成一个随机的UUID作为聊天ID
        id = str(uuid.uuid4())

        # 创建一个ChatModel对象，并将相关信息赋值给该对象
        chat = ChatModel(
            **{
                # 聊天ID
                "id": id,
                # 用户ID
                "user_id": user_id,
                # 聊天标题，如果form_data.chat中不包含"title"，则默认为"New Chat"
                "title": (
                    form_data.chat["title"] if "title" in form_data.chat else "New Chat"
                ),
                # 将form_data.chat转换为JSON字符串作为聊天内容
                "chat": json.dumps(form_data.chat),
                # 创建时间，取当前时间戳
                "created_at": int(time.time()),
                # 更新时间，取当前时间戳
                "updated_at": int(time.time()),
            }
        )
        # 调用Chat的create方法创建新的聊天记录，并返回结果
        try:
            result = Chat.create(**chat.model_dump()) # **是用来解构的
            # 更新redis聊天列表
            self.refresh_chat_redis(user_id)
        except Exception as e:
            print(1, e)
            

        # 如果创建成功，返回chat对象，否则返回None
        return chat if result else None

    def update_chat_by_id(self, id: str, chat: dict) -> Optional[ChatModel]:
        try:
            query = Chat.update(
                chat=json.dumps(chat),
                title=chat["title"] if "title" in chat else "New Chat",
                updated_at=int(time.time()),
            ).where(Chat.id == id)
            query.execute()

            chat = Chat.get(Chat.id == id)
            # 更新redis聊天列表
            self.refresh_chat_redis(chat.user_id)
            return ChatModel(**model_to_dict(chat))
        except:
            return None

    def insert_shared_chat_by_chat_id(self, chat_id: str) -> Optional[ChatModel]:
        # Get the existing chat to share
        chat = Chat.get(Chat.id == chat_id)
        # Check if the chat is already shared
        if chat.share_id:
            return self.get_chat_by_id_and_user_id(chat.share_id, "shared")
        # Create a new chat with the same data, but with a new ID
        shared_chat = ChatModel(
            **{
                "id": str(uuid.uuid4()),
                "user_id": f"shared-{chat_id}",
                "title": chat.title,
                "chat": chat.chat,
                "created_at": chat.created_at,
                "updated_at": int(time.time()),
            }
        )
        shared_result = Chat.create(**shared_chat.model_dump())
        # Update the original chat with the share_id
        result = (
            Chat.update(share_id=shared_chat.id).where(Chat.id == chat_id).execute()
        )

        return shared_chat if (shared_result and result) else None

    def update_shared_chat_by_chat_id(self, chat_id: str) -> Optional[ChatModel]:
        try:
            print("update_shared_chat_by_id")
            chat = Chat.get(Chat.id == chat_id)
            print(chat)

            query = Chat.update(
                title=chat.title,
                chat=chat.chat,
            ).where(Chat.id == chat.share_id)

            query.execute()

            chat = Chat.get(Chat.id == chat.share_id)
            return ChatModel(**model_to_dict(chat))
        except:
            return None

    def delete_shared_chat_by_chat_id(self, chat_id: str) -> bool:
        try:
            query = Chat.delete().where(Chat.user_id == f"shared-{chat_id}")
            query.execute()  # Remove the rows, return number of rows removed.
            return True
        except:
            return False

    def update_chat_share_id_by_id(
        self, id: str, share_id: Optional[str]
    ) -> Optional[ChatModel]:
        try:
            query = Chat.update(
                share_id=share_id,
            ).where(Chat.id == id)
            query.execute()

            chat = Chat.get(Chat.id == id)
            return ChatModel(**model_to_dict(chat))
        except:
            return None

    def toggle_chat_archive_by_id(self, id: str) -> Optional[ChatModel]:
        try:
            chat = self.get_chat_by_id(id)
            query = Chat.update(
                archived=(not chat.archived),
            ).where(Chat.id == id)

            query.execute()

            chat = Chat.get(Chat.id == id)
            return ChatModel(**model_to_dict(chat))
        except:
            return None

    def get_archived_chat_list_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 50
    ) -> List[ChatModel]:
        return [
            ChatModel(**model_to_dict(chat))
            for chat in Chat.select()
            .where(Chat.archived == True)
            .where(Chat.user_id == user_id)
            .order_by(Chat.updated_at.desc())
            # .limit(limit)
            # .offset(skip)
        ]

    @aspect_database_operations
    def get_chat_list_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 50
    ) -> List[ChatModel]:
        chat_dicts = RedisClientInstance.get_value_by_key(f"chat:{user_id}")
        if chat_dicts is None:
            chats = Chat.select(Chat.id, Chat.user_id, Chat.title, Chat.archived, Chat.created_at, Chat.updated_at).where(Chat.archived == False).where(Chat.user_id == user_id).order_by(Chat.updated_at.desc())
            chat_dicts = [model_to_dict(chat) for chat in chats]
            RedisClientInstance.add_key_value(f"chat:{user_id}", chat_dicts)
            chat_list = [ChatModel(**chat_dict) for chat_dict in chat_dicts]
            return chat_list
        else:
            chat_list = [ChatModel(**chat_dict) for chat_dict in chat_dicts]
            return chat_list

    def get_chat_list_by_chat_ids(
        self, chat_ids: List[str], skip: int = 0, limit: int = 50
    ) -> List[ChatModel]:
        return [
            ChatModel(**model_to_dict(chat))
            for chat in Chat.select()
            .where(Chat.archived == False)
            .where(Chat.id.in_(chat_ids))
            .order_by(Chat.updated_at.desc())
        ]
    
    def refresh_chat_redis(self, user_id: str):
        chats = Chat.select(Chat.id, Chat.user_id, Chat.title, Chat.archived, Chat.created_at, Chat.updated_at).where(Chat.archived == False).where(Chat.user_id == user_id).order_by(Chat.updated_at.desc())
        chat_dicts = [model_to_dict(chat) for chat in chats]
        RedisClientInstance.add_key_value(f"chat:{user_id}", chat_dicts)

    def get_chat_by_id(self, id: str) -> Optional[ChatModel]:
        try:
            chat = Chat.get(Chat.id == id)
            return ChatModel(**model_to_dict(chat))
        except:
            return None

    def get_chat_by_share_id(self, id: str) -> Optional[ChatModel]:
        try:
            chat = Chat.get(Chat.share_id == id)

            if chat:
                chat = Chat.get(Chat.id == id)
                return ChatModel(**model_to_dict(chat))
            else:
                return None
        except:
            return None

    def get_chat_by_id_and_user_id(self, id: str, user_id: str) -> Optional[ChatModel]:
        try:
            chat = Chat.get(Chat.id == id, Chat.user_id == user_id)
            return ChatModel(**model_to_dict(chat))
        except:
            return None

    def get_chats(self, skip: int = 0, limit: int = 50) -> List[ChatModel]:
        return [
            ChatModel(**model_to_dict(chat))
            for chat in Chat.select().order_by(Chat.updated_at.desc())
            # .limit(limit).offset(skip)
        ]

    def get_chats_by_user_id(self, user_id: str) -> List[ChatModel]:
        return [
            ChatModel(**model_to_dict(chat))
            for chat in Chat.select()
            .where(Chat.user_id == user_id)
            .order_by(Chat.updated_at.desc())
            # .limit(limit).offset(skip)
        ]

    def delete_chat_by_id(self, id: str) -> bool:
        try:
            # 获取chat信息
            chat = Chat.get(Chat.id == id)
            if chat is not None:
                query = Chat.delete().where((Chat.id == id))
                query.execute()  # Remove the rows, return number of rows removed.
                flag = True and self.delete_shared_chat_by_chat_id(id)
            # 更新redis聊天列表
            self.refresh_chat_redis(chat.user_id)   
            return flag
        except:
            return False

    def delete_chat_by_id_and_user_id(self, id: str, user_id: str) -> bool:
        try:
            query = Chat.delete().where((Chat.id == id) & (Chat.user_id == user_id))
            query.execute()  # Remove the rows, return number of rows removed.
            flag = True and self.delete_shared_chat_by_chat_id(id)
            # 更新redis聊天列表
            self.refresh_chat_redis(user_id) 
            return flag
        except:
            return False

    def delete_chats_by_user_id(self, user_id: str) -> bool:
        try:
            self.delete_shared_chats_by_user_id(user_id)
            query = Chat.delete().where(Chat.user_id == user_id)
            query.execute()  # Remove the rows, return number of rows removed.
            # 更新redis聊天列表
            self.refresh_chat_redis(user_id)
            return True
        except:
            return False

    def delete_shared_chats_by_user_id(self, user_id: str) -> bool:
        try:
            shared_chat_ids = [
                f"shared-{chat.id}"
                for chat in Chat.select().where(Chat.user_id == user_id)
            ]

            query = Chat.delete().where(Chat.user_id << shared_chat_ids)
            query.execute()  # Remove the rows, return number of rows removed.
            # 更新redis聊天列表
            self.refresh_chat_redis(user_id)
            return True
        except:
            return False


Chats = ChatTable(DB)
