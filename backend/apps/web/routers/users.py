from fastapi import Response, Request
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta, date
from typing import List, Union, Optional, Any

from fastapi import APIRouter
from pydantic import BaseModel
import logging

from apps.web.models.users import UserModel, UserUpdateForm, UserRoleUpdateForm, Users, UserRoleUpdateProForm, UserModelsUpdateForm, ChannelTotalModel, UserTotalModel, UserDisperModel, UserLanguageUpdateForm
from apps.web.models.auths import Auths
from apps.web.models.chats import Chats
from apps.web.models.rewards import RewardsTableInstance
from apps.web.models.vip import VIPStatuses, VIPStatusModelResp, VipTotalModel

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


# --------Wallet related--------
from web3 import Web3
#w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))  # Old Ethereum mainnet
w3 = Web3(Web3.HTTPProvider('https://rpc.dbcwallet.io')) # New Ethereum mainnet

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
# Get invited users for search
############################
@router.get("/invited", response_model=List[UserModel])
async def get_users_invited(
    session_user=Depends(get_current_user)
):
    
    # session_user = get_current_user()
    
    if session_user:
        print("session_user", session_user.id)
        try:
            users = Users.get_users_invited(session_user.id)
            print("users", users)
            return users
        except Exception as e:
            print("An error occurred while obtaining all invited users", e)
            raise HTTPException(400, detail="Error retrieving invited users")
    else:
        raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)


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
                start_date=start_date,
                end_date=end_date,
                order_id=tx_hash
            )
            print(f"New VIP created successfully: {new_vip_status}")
    except Exception as e:
        print("Update VIP error:", e)
        raise HTTPException(400, detail="update_user_vip error")



# Upgrade to Pro
@router.post("/pro", response_model=bool)
async def openPro(form_data: UserRoleUpdateProForm, session_user=Depends(get_current_user)):

    if session_user:
        try:
            # Obtain transaction hash information
            tx_hash = form_data.tx
            # tx = w3.eth.get_transaction(tx_hash)
            
            tx_receipt = await asyncio.to_thread(w3.eth.wait_for_transaction_receipt, tx_hash)
            # print("receipt", tx_receipt)
            print("receipt", tx_receipt)

            if tx_receipt.status == 1:
                # Analyze event logs
                for log in tx_receipt['logs']:
                    # Print log information
                    print(log)
                        
                    # Resolve the target address in the log (assuming the target address is included in the contract event)
                    # This needs to be analyzed based on your specific contract and event definition
                    # For example, if your contract event is defined as：event Transfer(address indexed from, address indexed to, uint256 value);
                    event_signature_hash = w3.keccak(text='Transfer(address,address,uint256)').hex()
                    if log['topics'][0].hex() == event_signature_hash:
                        from_address_hex = log['topics'][1].hex()
                        to_address_hex = log['topics'][2].hex()

                        # Processing address
                        from_address_hex = from_address_hex[26:]
                        to_address_hex = to_address_hex[26:]

                        from_address = w3.to_checksum_address('0x' + from_address_hex)
                        to_address = w3.to_checksum_address('0x' + to_address_hex)
                            
                        print(f"From: {from_address}")
                        print(f"To: {to_address}")
                            
                        if to_address == "0x2e0a85CB5352d7C542D632EdB4949DF879f8e981": 
                            print("execute update_user_vip")
                            update_user_vip(session_user.id, tx_hash)
                            # Users.update_user_role_by_id(session_user.id, "pro")
                            return True             
                else:
                    return False

        except Exception as e:
            print("An error occurred while obtaining all invited users", e)
            raise HTTPException(400, detail="Error retrieving invited users")
  

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

@router.post("/is_pro", response_model=Optional[VIPStatusModelResp])
async def isPro(session_user=Depends(get_current_user)):
    # print("isPro session_user", session_user)
    if session_user:
        try:
            user_id = session_user.id
            # print("user_id", user_id, session_user.id, session_user.role)
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
            print("Error in obtaining user information:", e)
            raise HTTPException(400, detail="Error get_user_info")

# Update user selection model       
@router.post("/update/models", response_model=bool)
async def update_user_role(form_data: UserModelsUpdateForm, user=Depends(get_current_user)):

    if user is not None:
        return Users.update_user_models(user.id, form_data.models)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

# Update user selection language       
@router.post("/update/language", response_model=bool)
async def update_user_role(form_data: UserLanguageUpdateForm, user=Depends(get_current_user)):

    if user is not None:
        return Users.update_user_language(user.id, form_data.language)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

# Obtain user registration distribution     
@router.post("/disper/total", response_model=UserTotalModel)
async def disper_total(user=Depends(get_current_user)):

    if user is not None:
        return Users.get_user_total()

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

# Obtain the distribution of user data in the past 15 days     
@router.post("/disper/user", response_model=UserDisperModel)
async def disper_total(user=Depends(get_current_user)):

    if user is not None:
        # Retrieve the previous 15 days' dates and store them in a list in month day format
        date_list = []
        today = datetime.today()
        for i in range(15):
            date = today - timedelta(days=14-i)
            date_list.append(date.strftime('%m-%d'))
        
        # Obtain user registration data for the past 15 days
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

# Obtain VIP upgrade distribution     
@router.post("/disper/vip", response_model=VipTotalModel)
async def disper_total(user=Depends(get_current_user)):

    if user is not None:
        return VIPStatuses.get_vip_total()

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

# Obtain third-party registration statistics data      
@router.post("/third/total", response_model=List[ChannelTotalModel])
async def third_total(user=Depends(get_current_user)):

    if user is not None:
        return Users.get_third_group_total()

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ERROR_MESSAGES.ACTION_PROHIBITED,
    )

# Obtain user registration reward statistics data      
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


# Verify if the user has followed their Twitter account 
@router.get("/check/twitter", response_model=bool)
async def third_total(request: Request):
    account = request.query_params.get("account")
    return TwitterApi.check_follow_status(account, "service@decentralgpt.org")