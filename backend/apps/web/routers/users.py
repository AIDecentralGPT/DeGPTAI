from fastapi import Response, Request
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta, date
from typing import List, Union, Optional, Any

from fastapi import APIRouter
from pydantic import BaseModel
import time
import uuid
import logging

from apps.web.models.users import UserModel, UserUpdateForm, UserRoleUpdateForm, Users, UserRoleUpdateProForm
from apps.web.models.auths import Auths
from apps.web.models.chats import Chats
from apps.web.models.vip import VIPStatuses, VIPStatusModelResp

from utils.utils import get_verified_user, get_password_hash, get_admin_user
from constants import ERROR_MESSAGES

from config import SRC_LOG_LEVELS

from utils.utils import (
    get_password_hash,
    get_current_user,
    get_admin_user,
    create_token,
    create_api_key,
)

from utils.misc import parse_duration, validate_email_format


# --------钱包相关--------
from substrateinterface import Keypair, KeypairType
from substrateinterface.utils.ss58 import ss58_decode
from substrateinterface.utils.hasher import blake2_256
import json
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))  # 使用以太坊主网
# from web3.auto import w3
from eth_account.messages import encode_defunct, _hash_eip191_message
import asyncio




log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

############################
# GetUsers
############################


# @router.get("/", response_model=List[UserModel])
@router.get("/", response_model=dict)
async def get_users(skip: int = 0, limit: int = 50, role: str = "", search: str = "", user=Depends(get_admin_user)):
    print("skip", skip, "limit", limit)
    return Users.get_users(skip, limit, role, search)

############################
# 获取搜有邀请用户
############################
@router.get("/invited", response_model=List[UserModel])
async def get_users_invited(
    session_user=Depends(get_current_user)
):
    # print("开始111")
    
    # session_user = get_current_user()
    print("session_user获取到啦111")
    
    if session_user:
        print("session_user", session_user.id)
        try:
            # 在这里添加你的业务逻辑，比如查询数据库
            users = Users.get_users_invited(session_user.id)
            print("users", users)
            return users
        except Exception as e:
            print("获取所有邀请用户时发生错误", e)
            raise HTTPException(400, detail="Error retrieving invited users")
    else:
        raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)


# @router.get("/users/invited", response_model=List[UserModel])
# async def get_users_invited(
#     session_user=Depends(get_current_user)
# ):
#     print("session_user获取到啦111")
    
#     print("session_user获取到啦", session_user.id)
#     if session_user:
#         try:
#             print("session_user", session_user.id)
#             # users = Users.get_users_invited(session_user.id)
#             # print("users", users)
#             return []
#         except Exception as e:
#             print("获取搜有邀请用户", e)
#         # if users:
#         #     return users
#         else:
#             raise HTTPException(400, detail=ERROR_MESSAGES.DEFAULT())
#     else:
#         raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)




############################
# User Permissions
############################


@router.get("/permissions/user")
async def get_user_permissions(request: Request, user=Depends(get_admin_user)):
    return request.app.state.config.USER_PERMISSIONS


@router.post("/permissions/user")
async def update_user_permissions(
    request: Request, form_data: dict, user=Depends(get_admin_user)
):
    request.app.state.config.USER_PERMISSIONS = form_data
    return request.app.state.config.USER_PERMISSIONS


############################
# UpdateUserRole
############################


@router.post("/update/role", response_model=Optional[UserModel])
async def update_user_role(form_data: UserRoleUpdateForm, user=Depends(get_admin_user)):

    if user.id != form_data.id and form_data.id != Users.get_first_user().id:
        return Users.update_user_role_by_id(form_data.id, form_data.role)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )


############################
# GetUserById
############################


class UserResponse(BaseModel):
    name: str
    profile_image_url: str


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, user=Depends(get_verified_user)):

    if user_id.startswith("shared-"):
        chat_id = user_id.replace("shared-", "")
        chat = Chats.get_chat_by_id(chat_id)
        if chat:
            user_id = chat.user_id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.USER_NOT_FOUND,
            )

    user = Users.get_user_by_id(user_id)

    if user:
        return UserResponse(name=user.name, profile_image_url=user.profile_image_url)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.USER_NOT_FOUND,
        )


############################
# UpdateUserById
############################


@router.post("/{user_id}/update", response_model=Optional[UserModel])
async def update_user_by_id(
    user_id: str, form_data: UserUpdateForm, session_user=Depends(get_admin_user)
):
    user = Users.get_user_by_id(user_id)

    if user:
        if form_data.email.lower() != user.email:
            email_user = Users.get_user_by_email(form_data.email.lower())
            if email_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ERROR_MESSAGES.EMAIL_TAKEN,
                )

        if form_data.password:
            hashed = get_password_hash(form_data.password)
            log.debug(f"hashed: {hashed}")
            Auths.update_user_password_by_id(user_id, hashed)

        Auths.update_email_by_id(user_id, form_data.email.lower())
        updated_user = Users.update_user_by_id(
            user_id,
            {
                "name": form_data.name,
                "email": form_data.email.lower(),
                "profile_image_url": form_data.profile_image_url,
            },
        )

        if updated_user:
            return updated_user

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(),
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.USER_NOT_FOUND,
    )


############################
# DeleteUserById
############################


@router.delete("/{user_id}", response_model=bool)
async def delete_user_by_id(user_id: str, user=Depends(get_admin_user)):
    if user.id != user_id:
        result = Auths.delete_auth_by_id(user_id)

        if result:
            return True

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES.DELETE_USER_ERROR,
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

def get_transaction_receipt(tx_hash):
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    if receipt:
        status = receipt['status']
        if status == 1:
            print("Transaction was successful")
        else:
            print("Transaction failed")
        return receipt
    else:
        print("Transaction receipt not found")
        return None



# def update_user_vip(user_id, tx_hash):
#     try:

#         # 插入新的VIP状态
#         new_vip_status = VIPStatuses.insert_vip_status(
#             user_id=user_id,
#             start_date=date(2024, 1, 1),
#             end_date=date(2025, 1, 1),
#             order_id=tx_hash
#         )
#         print(new_vip_status)

#         # 获取用户的VIP状态
#         vip_status = VIPStatuses.get_vip_status_by_user_id(user_id)
#         print(vip_status)

#         # 更新VIP结束日期
#         updated = VIPStatuses.update_vip_end_date(user_id, date(2025, 12, 31))
#         print(f"Update successful: {updated}")

#         # 检查VIP状态是否有效
#         is_active = VIPStatuses.is_vip_active(user_id)
#         print(f"VIP is active: {is_active}")
#     except Exception as e:
#         print("更新vip报错", e)
#         raise HTTPException(400, detail="update_user_vip error")


def update_user_vip(user_id, tx_hash):
    try:
        # 获取当前时间并计算一个月后的日期
        start_date = datetime.now().date()
        end_date = (datetime.now() + timedelta(days=30)).date()

        # 获取用户的VIP状态
        vip_status = VIPStatuses.get_vip_status_by_user_id(user_id)
        
        if vip_status and VIPStatuses.is_vip_active(user_id):
            # 用户已经是VIP，续费一个月
            new_end_date = vip_status.end_date + timedelta(days=30)
            updated = VIPStatuses.update_vip_end_date(user_id, new_end_date)
            print(f"VIP续费成功，新结束日期: {new_end_date}, 更新结果: {updated}")
        else:
            # 用户不是VIP，创建新的VIP状态并设置时长为一个月
            new_vip_status = VIPStatuses.insert_vip_status(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                order_id=tx_hash
            )
            print(f"新VIP创建成功: {new_vip_status}")

        # # 插入付费日志
        # new_payment_log = PaymentLogs.insert_payment_log(
        #     user_id=user_id,
        #     payment_date=datetime.now(),
        #     order_id=tx_hash
        # )
        # print(f"付费日志记录成功: {new_payment_log}")

    except Exception as e:
        print("更新vip报错", e)
        raise HTTPException(400, detail="update_user_vip error")



# 升级为pro
@router.post("/pro", response_model=bool)
async def openPro(form_data: UserRoleUpdateProForm, session_user=Depends(get_current_user)):

    if session_user:
        try:
            # # 在这里添加你的业务逻辑，比如查询数据库
            # users = Users.get_users_invited(session_user.id)
            # print("users", users)

            tx_hash = form_data.tx
            tx = w3.eth.get_transaction(tx_hash)
                
                
            # try:
            tx_receipt = await asyncio.to_thread(w3.eth.wait_for_transaction_receipt, tx_hash)
            print("receipt", tx_receipt)


            if tx_receipt.status == 1:
                # # 获取交易回执
                # tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
                # 打印交易回执
                print("Transaction Receipt:", tx_receipt)
                # 解析事件日志
                for log in tx_receipt['logs']:
                    # 打印日志信息
                    print(log)
                        
                    # 解析日志中的目标地址（假设合约事件中包含目标地址）
                    # 这里需要根据你的具体合约和事件定义进行解析
                    # 比如，如果你的合约事件定义为：event Transfer(address indexed from, address indexed to, uint256 value);
                    event_signature_hash = w3.keccak(text='Transfer(address,address,uint256)').hex()
                    if log['topics'][0].hex() == event_signature_hash:
                        from_address_hex = log['topics'][1].hex()
                        to_address_hex = log['topics'][2].hex()

                        # 处理地址
                        from_address_hex = from_address_hex[26:]
                        to_address_hex = to_address_hex[26:]

                        from_address = w3.to_checksum_address('0x' + from_address_hex)
                        to_address = w3.to_checksum_address('0x' + to_address_hex)
                            
                        print(f"From: {from_address}")
                        print(f"To: {to_address}")
                            
                        if to_address == "0x75A877EAB8CbD11836E27A137f7d0856ab8b90f8": 
                            print("执行update_user_vip")
                            update_user_vip(session_user.id, tx_hash)
                                # Users.update_user_role_by_id(session_user.id, "pro")


                            return True             
                else:
                    return False

        except Exception as e:
            print("获取所有邀请用户时发生错误", e)
            raise HTTPException(400, detail="Error retrieving invited users")
  

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )



@router.post("/is_pro", response_model=Optional[VIPStatusModelResp])
async def isPro( session_user=Depends(get_current_user)):
    # print("isPro session_user", session_user)
    if session_user:
        try:
            user_id = session_user.id
            # print("user_id", user_id, session_user.id, session_user.role)
            # 获取用户的VIP状态
            vip_status = VIPStatuses.get_vip_status_by_user_id(user_id)
            # print("vip_status", vip_status)
            # is_pro = vip_status and VIPStatuses.is_vip_active(user_id)
            if vip_status is None:
                return None;
            is_pro = bool(vip_status and VIPStatuses.is_vip_active(user_id))

            # print("isPro", is_pro, vip_status, VIPStatuses.is_vip_active(user_id), user_id, session_user.id, session_user.role)
            vip_status.is_pro = is_pro
            return vip_status
        except Exception as e:
            print("判断是否为vip", e)
            raise HTTPException(400, detail="Error is_pro")
            


@router.post("/get_user_info",response_model=None)
async def get_user_info(request: Request,  user=Depends(get_current_user)):
    # print("isPro session_user", session_user)
    if user:
        try:
            token = create_token(
                    data={"id": user.id},
                    expires_delta=parse_duration(request.app.state.config.JWT_EXPIRES_IN),
            )
            response = {
                "token": token,
                "token_type": "Bearer",
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "profile_image_url": user.profile_image_url,
                "address_type": user.address_type,
            }
            return response
                    
        except Exception as e:
            print("获取用户信息报错", e)
            raise HTTPException(400, detail="Error get_user_info")
            


