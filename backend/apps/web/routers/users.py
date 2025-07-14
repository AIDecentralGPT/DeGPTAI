from fastapi import Response, Request
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta, date
<<<<<<< HEAD
=======
from dateutil.relativedelta import relativedelta
>>>>>>> fingerprintAuth-out
from typing import List, Union, Optional, Any

from fastapi import APIRouter
from pydantic import BaseModel
import logging

from apps.web.models.users import UserModel, UserUpdateForm, UserRoleUpdateForm, Users, UserRoleUpdateProForm, UserModelsUpdateForm, ChannelTotalModel, UserTotalModel, UserDisperModel, UserLanguageUpdateForm
from apps.web.models.auths import Auths
from apps.web.models.chats import Chats
from apps.web.models.rewards import RewardsTableInstance
<<<<<<< HEAD
from apps.web.models.vip import VIPStatuses, VIPStatusModelResp, VipTotalModel
=======
from apps.web.models.vipstatus import VIPStatuses, VIPStatusModelResp, VipTotalModel
>>>>>>> fingerprintAuth-out

from utils.utils import get_verified_user, get_password_hash, get_admin_user
from constants import ERROR_MESSAGES

from config import SRC_LOG_LEVELS

from utils.utils import (
    get_password_hash,
    get_current_user,
    get_admin_user,
    create_token,
)

from utils.misc import parse_duration, validate_email_format


<<<<<<< HEAD
# --------Wallet related--------
from web3 import Web3
#w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))  # Old Ethereum mainnet
w3 = Web3(Web3.HTTPProvider('https://rpc.dbcwallet.io')) # New Ethereum mainnet
=======
# --------钱包相关--------
from web3 import Web3
#w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))  # 旧以太坊主网
w3 = Web3(Web3.HTTPProvider('https://rpc1.dbcwallet.io')) # 新以太坊主网
>>>>>>> fingerprintAuth-out

# from web3.auto import w3
import asyncio

from apps.web.api.twitter import TwitterApi




log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

############################
# GetUsers
############################


# @router.get("/", response_model=List[UserModel])
@router.get("/", response_model=dict)
async def get_users(skip: int = 0, limit: int = 50, role: str = "", search: str = "", verified: str = "", channel: str = "", user=Depends(get_admin_user)):
    print("skip", skip, "limit", limit)
    return Users.get_users(skip, limit, role, search, verified, channel)

############################
<<<<<<< HEAD
# Get invited users for search
=======
# 获取搜有邀请用户
>>>>>>> fingerprintAuth-out
############################
@router.get("/invited", response_model=List[UserModel])
async def get_users_invited(
    session_user=Depends(get_current_user)
):
<<<<<<< HEAD
    
    # session_user = get_current_user()
=======
    # print("开始111")
    
    # session_user = get_current_user()
    print("session_user获取到啦111")
>>>>>>> fingerprintAuth-out
    
    if session_user:
        print("session_user", session_user.id)
        try:
<<<<<<< HEAD
=======
            # 在这里添加你的业务逻辑，比如查询数据库
>>>>>>> fingerprintAuth-out
            users = Users.get_users_invited(session_user.id)
            print("users", users)
            return users
        except Exception as e:
<<<<<<< HEAD
            print("An error occurred while obtaining all invited users", e)
=======
            print("获取所有邀请用户时发生错误", e)
>>>>>>> fingerprintAuth-out
            raise HTTPException(400, detail="Error retrieving invited users")
    else:
        raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)


############################
# User Permissions
############################
<<<<<<< HEAD


=======
>>>>>>> fingerprintAuth-out
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
<<<<<<< HEAD


=======
>>>>>>> fingerprintAuth-out
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
<<<<<<< HEAD


=======
>>>>>>> fingerprintAuth-out
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
<<<<<<< HEAD


=======
>>>>>>> fingerprintAuth-out
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
<<<<<<< HEAD


=======
>>>>>>> fingerprintAuth-out
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


<<<<<<< HEAD
def update_user_vip(user_id, tx_hash):
    try:
        # Get the current time and calculate the date one month later
        start_date = datetime.now().date()
        end_date = (datetime.now() + timedelta(days=30)).date()

        # Obtain the VIP status of the user
        vip_status = VIPStatuses.get_vip_status_by_user_id(user_id)
        
        if vip_status and VIPStatuses.is_vip_active(user_id):
            # The user is already VIP, renew for one month
            new_end_date = vip_status.end_date + timedelta(days=30)
            updated = VIPStatuses.update_vip_end_date(user_id, new_end_date)
            print(f"VIP renewal successful, new end date: {new_end_date}, Update Results: {updated}")
        else:
            # The user is not VIP, create a new VIP status and set the duration to one month
            new_vip_status = VIPStatuses.insert_vip_status(
                user_id=user_id,
=======

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


def update_user_vip(user_id, tx_hash, vip, time):
    try:
        # 获取当前时间并计算一个月后的日期
        start_date = datetime.now().date()
        if (time == "month"):
            end_date = (datetime.now() + timedelta(days=30)).date()
        else:
            end_date = (datetime.now() + relativedelta(years=1)).date()

        # 获取用户的VIP状态
        vip_status = VIPStatuses.get_vip_status_by_userid_vip(user_id, vip)
        
        if vip_status:
            # 用户已经是VIP
            if (time == "month"):
                new_end_date = vip_status.end_date + timedelta(days=30)
            else:
                new_end_date = vip_status.end_date + relativedelta(years=1)
            
            VIPStatuses.update_vip_end_date(vip_status.id, new_end_date)
        else:
            # 用户不是VIP，创建新的VIP状态并设置时长为一个月
            level = 1
            if vip == "standard":
                level = 2
            elif vip == "pro":
                level = 3
            VIPStatuses.insert_vip_status(
                user_id=user_id,
                vip=vip,
                level=level,
>>>>>>> fingerprintAuth-out
                start_date=start_date,
                end_date=end_date,
                order_id=tx_hash
            )
<<<<<<< HEAD
            print(f"New VIP created successfully: {new_vip_status}")
    except Exception as e:
        print("Update VIP error:", e)
=======
            
    except Exception as e:
        print("更新vip报错", e)
>>>>>>> fingerprintAuth-out
        raise HTTPException(400, detail="update_user_vip error")



<<<<<<< HEAD
# Upgrade to Pro
@router.post("/pro", response_model=bool)
=======
# 升级为pro
@router.post("/pro")
>>>>>>> fingerprintAuth-out
async def openPro(form_data: UserRoleUpdateProForm, session_user=Depends(get_current_user)):

    if session_user:
        try:
<<<<<<< HEAD
            # Obtain transaction hash information
=======
            # 获取交易Hash信息
>>>>>>> fingerprintAuth-out
            tx_hash = form_data.tx
            # tx = w3.eth.get_transaction(tx_hash)
            
            tx_receipt = await asyncio.to_thread(w3.eth.wait_for_transaction_receipt, tx_hash)
            # print("receipt", tx_receipt)
            print("receipt", tx_receipt)

            if tx_receipt.status == 1:
<<<<<<< HEAD
                # Analyze event logs
                for log in tx_receipt['logs']:
                    # Print log information
                    print(log)
                        
                    # Resolve the target address in the log (assuming the target address is included in the contract event)
                    # This needs to be analyzed based on your specific contract and event definition
                    # For example, if your contract event is defined as：event Transfer(address indexed from, address indexed to, uint256 value);
=======
                # 解析事件日志
                for log in tx_receipt['logs']:
                    # 打印日志信息
                    print(log)
                        
                    # 解析日志中的目标地址（假设合约事件中包含目标地址）
                    # 这里需要根据你的具体合约和事件定义进行解析
                    # 比如，如果你的合约事件定义为：event Transfer(address indexed from, address indexed to, uint256 value);
>>>>>>> fingerprintAuth-out
                    event_signature_hash = w3.keccak(text='Transfer(address,address,uint256)').hex()
                    if log['topics'][0].hex() == event_signature_hash:
                        from_address_hex = log['topics'][1].hex()
                        to_address_hex = log['topics'][2].hex()

<<<<<<< HEAD
                        # Processing address
=======
                        # 处理地址
>>>>>>> fingerprintAuth-out
                        from_address_hex = from_address_hex[26:]
                        to_address_hex = to_address_hex[26:]

                        from_address = w3.to_checksum_address('0x' + from_address_hex)
                        to_address = w3.to_checksum_address('0x' + to_address_hex)
                            
                        print(f"From: {from_address}")
                        print(f"To: {to_address}")
                            
<<<<<<< HEAD
                        if to_address == "0x2e0a85CB5352d7C542D632EdB4949DF879f8e981": 
                            print("execute update_user_vip")
                            update_user_vip(session_user.id, tx_hash)
                            # Users.update_user_role_by_id(session_user.id, "pro")
                            return True             
                else:
                    return False

        except Exception as e:
            print("An error occurred while obtaining all invited users", e)
=======
                        if to_address == "0x40Ff2BD3668B38B0dd0BD7F26Aa809239Fc9113a": 
                            print("执行update_user_vip")
                            update_user_vip(session_user.id, tx_hash, form_data.vip, form_data.viptime)

                            # 获取VIP信息
                            viplist = VIPStatuses.get_vip_status_by_user_id(session_user.id)
                            return {"ok": True, "data": viplist}
                else:
                    return {"ok": False, "data": []}

        except Exception as e:
            print("============upgradeVip==========", e)
>>>>>>> fingerprintAuth-out
            raise HTTPException(400, detail="Error retrieving invited users")
  

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

<<<<<<< HEAD
@router.post("/is_pro", response_model=Optional[VIPStatusModelResp])
=======
@router.post("/is_pro", response_model=Optional[List[VIPStatusModelResp]])
>>>>>>> fingerprintAuth-out
async def isPro(session_user=Depends(get_current_user)):
    # print("isPro session_user", session_user)
    if session_user:
        try:
            user_id = session_user.id
            # print("user_id", user_id, session_user.id, session_user.role)
<<<<<<< HEAD
            # Obtain the VIP status of the user
            vip_status = VIPStatuses.get_vip_status_by_user_id(user_id)
            # print("vip_status", vip_status)
            # is_pro = vip_status and VIPStatuses.is_vip_active(user_id)
            if vip_status is None:
                return None
            is_pro = bool(vip_status and VIPStatuses.is_vip_active(user_id))

            # print("isPro", is_pro, vip_status, VIPStatuses.is_vip_active(user_id), user_id, session_user.id, session_user.role)
            vip_status.is_pro = is_pro
            return vip_status
        except Exception as e:
            print("Determine if it is VIP:", e)
=======
            # 获取用户的VIP状态
            vip_status = VIPStatuses.get_vip_status_by_user_id(user_id)
            return vip_status
        except Exception as e:
            print("判断是否为vip", e)
>>>>>>> fingerprintAuth-out
            raise HTTPException(400, detail="Error is_pro")
            


@router.post("/get_user_info",response_model=None)
async def get_user_info(request: Request,  user=Depends(get_current_user)):
    # print("isPro session_user", session_user)
    if user:
        try:
            response = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "profile_image_url": user.profile_image_url,
                "address_type": user.address_type,
                "verified": user.verified,
                "models": user.models,
                "language": user.language
            }
            return response
                    
        except Exception as e:
<<<<<<< HEAD
            print("Error in obtaining user information:", e)
            raise HTTPException(400, detail="Error get_user_info")

# Update user selection model       
=======
            print("获取用户信息报错", e)
            raise HTTPException(400, detail="Error get_user_info")

# 更新用户选择模型       
>>>>>>> fingerprintAuth-out
@router.post("/update/models", response_model=bool)
async def update_user_role(form_data: UserModelsUpdateForm, user=Depends(get_current_user)):

    if user is not None:
        return Users.update_user_models(user.id, form_data.models)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

<<<<<<< HEAD
# Update user selection language       
=======
# 更新用户选择语言       
>>>>>>> fingerprintAuth-out
@router.post("/update/language", response_model=bool)
async def update_user_role(form_data: UserLanguageUpdateForm, user=Depends(get_current_user)):

    if user is not None:
        return Users.update_user_language(user.id, form_data.language)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

<<<<<<< HEAD
# Obtain user registration distribution     
=======
# 获取用户注册分布     
>>>>>>> fingerprintAuth-out
@router.post("/disper/total", response_model=UserTotalModel)
async def disper_total(user=Depends(get_current_user)):

    if user is not None:
        return Users.get_user_total()

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

<<<<<<< HEAD
# Obtain the distribution of user data in the past 15 days     
=======
# 获取近15天用户数据分布     
>>>>>>> fingerprintAuth-out
@router.post("/disper/user", response_model=UserDisperModel)
async def disper_total(user=Depends(get_current_user)):

    if user is not None:
<<<<<<< HEAD
        # Retrieve the previous 15 days' dates and store them in a list in month day format
=======
        # 获取前15天日期并以月日格式存储在列表中
>>>>>>> fingerprintAuth-out
        date_list = []
        today = datetime.today()
        for i in range(15):
            date = today - timedelta(days=14-i)
            date_list.append(date.strftime('%m-%d'))
        
<<<<<<< HEAD
        # Obtain user registration data for the past 15 days
=======
        # 获取用户注册数近15天数据
>>>>>>> fingerprintAuth-out
        users = Users.get_user_lately()
        wallet_list = []
        channel_list = []
        kyc_list = []
        for date in date_list:
            userlately = [user for user in users if user.create_date == date]
            if len(userlately) > 0:
                wallet_list.append(userlately[0].wallet_count)
                channel_list.append(userlately[0].channel_count)
                kyc_list.append(userlately[0].kyc_count)
            else:
                wallet_list.append(0)
                channel_list.append(0)
                kyc_list.append(0)

        data = {
            "date_list": date_list,
            "wallet_list": wallet_list,
            "channel_list": channel_list,
            "kyc_list": kyc_list
        }
        return UserDisperModel(**data)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

<<<<<<< HEAD
# Obtain VIP upgrade distribution     
=======
# 获取VIP升级分布     
>>>>>>> fingerprintAuth-out
@router.post("/disper/vip", response_model=VipTotalModel)
async def disper_total(user=Depends(get_current_user)):

    if user is not None:
        return VIPStatuses.get_vip_total()

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

<<<<<<< HEAD
# Obtain third-party registration statistics data      
=======
# 获取第三方注册统计数据      
>>>>>>> fingerprintAuth-out
@router.post("/third/total", response_model=List[ChannelTotalModel])
async def third_total(user=Depends(get_current_user)):

    if user is not None:
        return Users.get_third_group_total()

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

<<<<<<< HEAD
# Obtain user registration reward statistics data      
=======
# 获取用户注册奖励统计数据      
>>>>>>> fingerprintAuth-out
@router.post("/regist/total")
async def regist_total(user=Depends(get_current_user)):

    if user is not None:
        regist_total = Users.get_regist_total()
        reward_total = Users.get_regist_reward_total()
        issue_total = RewardsTableInstance.get_issue_reward()
        return {
            "regist_total": regist_total,
            "reward_total": reward_total,
            "issue_total": issue_total
        }

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )


<<<<<<< HEAD
# Verify if the user has followed their Twitter account 
=======
# 校验用户是否已关注推特账号 
>>>>>>> fingerprintAuth-out
@router.get("/check/twitter", response_model=bool)
async def third_total(request: Request):
    account = request.query_params.get("account")
    return TwitterApi.check_follow_status(account, "service@decentralgpt.org")