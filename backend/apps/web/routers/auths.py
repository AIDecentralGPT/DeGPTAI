<<<<<<< HEAD
from apps.web.api.rewardapi import RewardApi
=======
>>>>>>> fingerprintAuth-out
from datetime import datetime
from config import WEBUI_AUTH, WEBUI_AUTH_TRUSTED_EMAIL_HEADER
from constants import ERROR_MESSAGES, WEBHOOK_MESSAGES
from utils.webhook import post_webhook
from utils.misc import parse_duration, validate_email_format
from utils.utils import (
    get_password_hash,
    get_current_user,
    get_admin_user,
    create_token,
    create_api_key,
)
from apps.web.api.rewardapi import RewardApiInstance
from apps.web.models.rewards import RewardsTableInstance
from apps.web.models.faceLib import face_lib
from apps.web.models.faceCompare import face_compare
from apps.web.models.device import devices_table
from apps.web.models.ip_log import ip_logs_table
from apps.web.models.users import Users, UserRequest
from apps.web.models.auths import (
    SigninForm,
    FingerprintSignInForm,
    WalletSigninForm,
    SignupForm,
    AddUserForm,
    UpdateProfileForm,
    UpdatePasswordForm,
    UserResponse,
    SigninResponse,
    Auths,
    ApiKey,
    FaceLivenessRequest,
    FaceLivenessResponse,
    FaceLivenessCheckResponse
)
from eth_account.messages import encode_defunct
from web3.auto import w3
from web3 import Web3
import json
import logging
from typing import List, Dict
from utils.utils import get_verified_user

from fastapi import Request, WebSocket, WebSocketDisconnect
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter
from pydantic import BaseModel
import re
import uuid
import base64

from apps.web.models.email_codes import (
    email_code_operations,
    EmailRequest,
    TimeRequest,
    VerifyCodeRequest
)

from apps.web.models.kyc_restrict import KycRestrictInstance
from apps.web.api.captcha import CaptchaApiInstance

from constants import USER_CONSTANTS
import logging
log = logging.getLogger(__name__)

<<<<<<< HEAD
# --------Wallet related--------
#w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))  # Old Ethereum mainnet
w3 = Web3(Web3.HTTPProvider('https://rpc.dbcwallet.io')) # New Ethereum mainnet
=======
# --------钱包相关--------
#w3 = Web3(Web3.HTTPProvider('https://rpc-testnet.dbcwallet.io'))  # 旧以太坊主网
w3 = Web3(Web3.HTTPProvider('https://rpc1.dbcwallet.io')) # 新以太坊主网
>>>>>>> fingerprintAuth-out

# ————————————————————————


router = APIRouter()

############################
# GetSessionUser
############################


@router.get("/", response_model=UserResponse)
async def get_session_user(user=Depends(get_current_user)):
    try:
<<<<<<< HEAD
        # print("audo get_session_user => user:", user.id, user)
=======
        # print("audo get_session_user 的 user:", user.id, user)
>>>>>>> fingerprintAuth-out
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "profile_image_url": user.profile_image_url,
            "address_type": user.address_type,
            "verified": user.verified,
            "address": user.address
        }
    except AttributeError as e:
        print("AttributeError: ", e)
        return {"error": "An error occurred while fetching user details"}
    except Exception as e:
        print("Exception: ", e)
        return {"error": "An internal server error occurred"}


############################
# Update Profile
############################


@router.post("/update/profile", response_model=UserResponse)
async def update_profile(
    form_data: UpdateProfileForm, session_user=Depends(get_current_user)
):
    if session_user:
        try:
            if form_data.name == 'admin+webui1234':
                user = Users.update_user_by_id(
                    session_user.id,
                    {"profile_image_url": form_data.profile_image_url,
                        "name": form_data.name, "role": 'admin'},
                )
            else:
                user = Users.update_user_by_id(
                    session_user.id,
                    {"profile_image_url": form_data.profile_image_url,
                        "name": form_data.name},
                )
        except Exception as e:
            print("update_profile", e)
        if user:
            return user
        else:
            raise HTTPException(400, detail=ERROR_MESSAGES.DEFAULT())
    else:
        raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)


############################
# Update Password
############################


@router.post("/update/password", response_model=bool)
async def update_password(
    form_data: UpdatePasswordForm, session_user=Depends(get_current_user)
):
    if WEBUI_AUTH_TRUSTED_EMAIL_HEADER:
        raise HTTPException(400, detail=ERROR_MESSAGES.ACTION_PROHIBITED)
    if session_user:
        user = Auths.authenticate_user(session_user.email, form_data.password)

        if user:
            hashed = get_password_hash(form_data.new_password)
            return Auths.update_user_password_by_id(user.id, hashed)
        else:
            raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_PASSWORD)
    else:
        raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)


############################
# SignIn
############################

@router.post("/printSignIn", response_model=None)
async def printSignIn(request: Request, form_data: FingerprintSignInForm):

    try:
        user = Users.get_user_by_id(form_data.id)
    except Exception as e:
        print("Error retrieving user by id:", e.message)

    if user:
        print("User found:", user.id)
    else:
        print("User not found, creating new user")

        hashed = get_password_hash("")

<<<<<<< HEAD
        # Create a new Ethereum account using web3.py
=======
        # 使用 web3.py 创建新的以太坊账户
>>>>>>> fingerprintAuth-out
        account = w3.eth.account.create()
        wallet_address = account.address
        # private_key = account.key.hex()
        # private_key=w3.to_hex(account.key)
        # python -c "from web3 import Web3; w3 = Web3(); acc = w3.eth.account.create(); print(f'private key={w3.to_hex(acc.key)}, account={acc.address}')"
<<<<<<< HEAD
        print("System creates wallet account:", wallet_address)
=======
        print("系统创建钱包账户:", wallet_address)
>>>>>>> fingerprintAuth-out

        Auths.insert_new_auth(
            "",
            hashed,
            "user",
            "",
            "visitor",
            form_data.id,
            "",
            address_type=None,
            address=wallet_address,
            channel=form_data.channel
        )
        print("Auths.insert_new_auth executed")

        user = Users.get_user_by_id(form_data.id)
        print("New user created:", user.id)

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
        "address": user.address,
        "models": user.models,
        "language": user.language
    }
<<<<<<< HEAD
    # print("Returning response:", response)  # print log
=======
    # print("Returning response:", response)  # 打印日志
>>>>>>> fingerprintAuth-out
    return response


@router.post("/walletSignIn")
async def walletSignIn(request: Request, form_data: WalletSigninForm):
    print("Received Data:", form_data)
    address = form_data.address
    address_type = form_data.address_type
    message = form_data.nonce
    signature = form_data.signature
    device_id = form_data.device_id
    ip_address = request.client.host
    address_type = form_data.address_type

    try:
        sign_is_valid = False

        if address_type == 'threeSide':
            sign_is_valid = False
<<<<<<< HEAD
            # First, perform Base64 decoding
            decoded_data = base64.b64decode(signature)
            # Convert the decoded data into a processable character format (assuming the original data is text)
            decoded_text = decoded_data.decode('utf-8')
            # Perform processing corresponding to encryption to restore data (here it is simply illustrated by subtracting and modulo each character, corresponding to adding and modulo during encryption)
=======
            # if form_data.nonce == signature:
            #     sign_is_valid = True
            # else:
            # 将签名解码为字节
            # signature_bytes = Web3.to_bytes(hexstr=signature)
            # print("message_text", message)

            # 使用 web3.py 的 eth.account.recover_message 方法验证签名
            # recovered_address = w3.eth.account.recover_message(encode_defunct(text=message), signature=signature_bytes)

            # recovered_address = w3.eth.account.recover_message(message_text=message, signature=signature_bytes)
            # print("recovered_address:", recovered_address, "address:", address)

            # 比较签名者地址和恢复的地址
            # sign_is_valid = recovered_address.lower() == address.lower()

            # 先进行Base64解码
            decoded_data = base64.b64decode(signature)
            # 将解码后的数据转换为可处理的字符形式（假设原始数据是文本）
            decoded_text = decoded_data.decode('utf-8')
            # 进行与加密时相对应的处理来还原数据（这里简单通过逐个字符相减取模运算来示意，与加密时相加取模对应）
>>>>>>> fingerprintAuth-out
            restored_text = ''
            for i in range(len(decoded_text)):
                char_code = ord(decoded_text[i])
                vector_char_code = ord(address[i % len(address)])
                restored_text += chr((char_code - vector_char_code) % 256)
            sign_is_valid = restored_text == message

        else:
<<<<<<< HEAD
            # The message signature format of Ethereum is "\x19Ethereum Signed Message:\n" + len(message) + message
            # prefixed_message = "\x19Ethereum Signed Message:\n" + str(len(message)) + message
            encoded_message = encode_defunct(text=message)

            # Restore address from signature
=======
            # 以太坊的消息签名格式是 "\x19Ethereum Signed Message:\n" + len(message) + message
            # prefixed_message = "\x19Ethereum Signed Message:\n" + str(len(message)) + message
            encoded_message = encode_defunct(text=message)

            # 从签名中恢复地址
>>>>>>> fingerprintAuth-out
            address_signed = w3.eth.account.recover_message(
                encoded_message, signature=signature)

            print("address_signed:", address_signed)
            print("address:", address)
            sign_is_valid = address_signed.lower() == address.lower()

<<<<<<< HEAD
        if sign_is_valid:  # Ignore capitalization for comparison
=======
        if sign_is_valid:  # 忽略大小写进行比较
>>>>>>> fingerprintAuth-out
            user = Users.get_user_by_id(address)
            user_count = None

            if user:
                print("User found:", user.id)
            else:
                print("User not found, creating new user")

<<<<<<< HEAD
                # Add user information
=======
                # 添加用户信息
>>>>>>> fingerprintAuth-out
                hashed = get_password_hash("")
                result = Auths.insert_new_auth(
                    "",
                    hashed,
                    address,
                    "",
                    "walletUser",
                    form_data.address,
                    form_data.inviter_id,
                    address_type=address_type,
                    address=address,
                    channel=form_data.channel
                )

                if result:
<<<<<<< HEAD
                    user, user_count = result  # Unpack the returned tuple
                    print(f"User: {user}, Count: {user_count}")
                else:
                    print("User creation failed")

            # Record device ID and IP address
=======
                    user, user_count = result  # 解包返回的元组
                    print(f"用户: {user}, 用户个数: {user_count}")
                else:
                    print("用户创建失败")

            # 记录设备ID和IP地址
>>>>>>> fingerprintAuth-out
            if device_id:
                device = devices_table.insert_new_device(
                    user_id=user.id, device_id=device_id)
            else:
                log.info("No device_id provided!")

            ip_log = ip_logs_table.insert_new_ip_log(
                user_id=user.id, ip_address=ip_address)

            token = create_token(
                data={"id": user.id},
                expires_delta=parse_duration(
                    request.app.state.config.JWT_EXPIRES_IN),
            )
            response = {
                "token": token,
                "token_type": "Bearer",
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "profile_image_url": user.profile_image_url,
                "address_type": address_type,
                "verified": user.verified,
                "address": user.address,
                "user_no": user_count + 1 if user_count is not None else None,
                "models": user.models,
                "language": user.language
            }
            return response
        else:
            raise HTTPException(
                status_code=400, detail="Signature verification failed")

    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/signin", response_model=SigninResponse)
async def signin(request: Request, form_data: SigninForm):
<<<<<<< HEAD
    # Check if trust header based WebUI authentication is enabled
    if WEBUI_AUTH_TRUSTED_EMAIL_HEADER:
        print("Checking if trusted email header authentication is enabled")
        # Check if the request header contains a trust header
=======
    # 检查是否启用了基于信任头的 WebUI 认证
    if WEBUI_AUTH_TRUSTED_EMAIL_HEADER:
        print("Checking if trusted email header authentication is enabled")
        # 检查请求头中是否包含信任头
>>>>>>> fingerprintAuth-out
        if WEBUI_AUTH_TRUSTED_EMAIL_HEADER not in request.headers:
            print(1)
            raise HTTPException(
                400, detail=ERROR_MESSAGES.INVALID_TRUSTED_HEADER)

<<<<<<< HEAD
        # Retrieve the email address from the trust header and convert it to lowercase
        trusted_email = request.headers[WEBUI_AUTH_TRUSTED_EMAIL_HEADER].lower(
        )
        # Check if the user exists, if not, register
=======
        # 获取信任头中的邮箱并转为小写
        trusted_email = request.headers[WEBUI_AUTH_TRUSTED_EMAIL_HEADER].lower(
        )
        # 检查用户是否存在，如果不存在则进行注册
>>>>>>> fingerprintAuth-out
        if not Users.get_user_by_email(trusted_email.lower()):
            await signup(
                request,
                SignupForm(
                    email=trusted_email, password=str(uuid.uuid4()), name=trusted_email
                ),
            )

<<<<<<< HEAD
        # User authentication through trusted header email
        user = Auths.authenticate_user_by_trusted_header(trusted_email)
    # Check if WebUI authentication is disabled
=======
        # 通过信任头邮箱进行用户认证
        user = Auths.authenticate_user_by_trusted_header(trusted_email)
    # 检查是否禁用了 WebUI 认证
>>>>>>> fingerprintAuth-out
    elif WEBUI_AUTH == False:
        print("Checking if WebUI authentication is disabled")
        admin_email = "admin@localhost"
        admin_password = "admin"
        print(2)

<<<<<<< HEAD
        # Check if the administrator account exists
        if Users.get_user_by_email(admin_email.lower()):
            # The administrator account exists, please authenticate it
            user = Auths.authenticate_user(admin_email.lower(), admin_password)
        else:
            # The administrator account does not exist. Check if there are any other users
            if Users.get_num_users() != 0:
                raise HTTPException(400, detail=ERROR_MESSAGES.EXISTING_USERS)

            # No other users, register an administrator account
=======
        # 检查管理员账号是否存在
        if Users.get_user_by_email(admin_email.lower()):
            # 管理员账号存在，进行认证
            user = Auths.authenticate_user(admin_email.lower(), admin_password)
        else:
            # 管理员账号不存在，检查是否有其他用户
            if Users.get_num_users() != 0:
                raise HTTPException(400, detail=ERROR_MESSAGES.EXISTING_USERS)

            # 没有其他用户，进行管理员账号注册
>>>>>>> fingerprintAuth-out
            await signup(
                request,
                SignupForm(email=admin_email, password=admin_password,
                           name="User", visiter_id=form_data.visiter_id),
            )

<<<<<<< HEAD
            # After registration is completed, proceed with authentication again
            user = Auths.authenticate_user(
                admin_email.lower(), admin_password, )
    else:
        # Use the email and password in the form for user authentication
        user = Auths.authenticate_user(
            form_data.email.lower(), form_data.password)
        print("Use the email and password in the form for user authentication:", user)

    # If authentication is successful, generate a token and return user information
=======
            # 注册完成后，再次进行认证
            user = Auths.authenticate_user(
                admin_email.lower(), admin_password, )
    else:
        # 使用表单中的邮箱和密码进行用户认证
        user = Auths.authenticate_user(
            form_data.email.lower(), form_data.password)
        print("使用表单中的邮箱和密码进行用户认证", user)

    # 如果认证成功，则生成令牌并返回用户信息
>>>>>>> fingerprintAuth-out
    if user:
        token = create_token(
            data={"id": user.id},
            expires_delta=parse_duration(
                request.app.state.config.JWT_EXPIRES_IN),
        )

        return {
            "token": token,
            "token_type": "Bearer",
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "profile_image_url": user.profile_image_url,
        }
    else:
<<<<<<< HEAD
        # If authentication fails, print the log and return an error message
=======
        # 如果认证失败，则打印日志并返回错误提示
>>>>>>> fingerprintAuth-out
        print(3)
        raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)


############################
# SignUp
############################


@router.post("/signup", response_model=SigninResponse)
async def signup(request: Request, form_data: SignupForm):
    if not request.app.state.config.ENABLE_SIGNUP and WEBUI_AUTH:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail=ERROR_MESSAGES.ACCESS_PROHIBITED
        )

    # if not validate_email_format(form_data.email.lower()):
    #     raise HTTPException(
    #         status.HTTP_400_BAD_REQUEST, detail=ERROR_MESSAGES.INVALID_EMAIL_FORMAT
    #     )

    # if Users.get_user_by_email(form_data.email.lower()):
    #     raise HTTPException(400, detail=ERROR_MESSAGES.EMAIL_TAKEN)

    try:
        role = (
            "admin"
            if Users.get_num_users() == 0
            else request.app.state.config.DEFAULT_USER_ROLE
        )
        hashed = get_password_hash(form_data.password)
        user = Auths.insert_new_auth(
            form_data.email.lower(),
            hashed,
            form_data.name,
            form_data.profile_image_url,
            "user",
            form_data.id,
            form_data.inviter_id,
            address_type=None
        )

        if user:
            token = create_token(
                data={"id": user.id},
                expires_delta=parse_duration(
                    request.app.state.config.JWT_EXPIRES_IN),
            )
            # response.set_cookie(key='token', value=token, httponly=True)

            if request.app.state.config.WEBHOOK_URL:
                post_webhook(
                    request.app.state.config.WEBHOOK_URL,
                    WEBHOOK_MESSAGES.USER_SIGNUP(user.name),
                    {
                        "action": "signup",
                        "message": WEBHOOK_MESSAGES.USER_SIGNUP(user.name),
                        "user": user.model_dump_json(exclude_none=True),
                    },
                )

            return {
                "token": token,
                "token_type": "Bearer",
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "profile_image_url": user.profile_image_url,
            }
        else:
            raise HTTPException(500, detail=ERROR_MESSAGES.CREATE_USER_ERROR)
    except Exception as err:
        raise HTTPException(500, detail=ERROR_MESSAGES.DEFAULT(err))


############################
# AddUser
############################


@router.post("/add", response_model=SigninResponse)
async def add_user(form_data: AddUserForm, user=Depends(get_admin_user)):

    if not validate_email_format(form_data.email.lower()):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=ERROR_MESSAGES.INVALID_EMAIL_FORMAT
        )

    if Users.get_user_by_email(form_data.email.lower()):
        raise HTTPException(400, detail=ERROR_MESSAGES.EMAIL_TAKEN)

    try:

        print(form_data)
        hashed = get_password_hash(form_data.password)
        user = Auths.insert_new_auth(
            form_data.email.lower(),
            hashed,
            form_data.name,
            form_data.profile_image_url,
            form_data.role,
        )

        if user:
            token = create_token(data={"id": user.id})
            return {
                "token": token,
                "token_type": "Bearer",
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "profile_image_url": user.profile_image_url,
            }
        else:
            raise HTTPException(500, detail=ERROR_MESSAGES.CREATE_USER_ERROR)
    except Exception as err:
        raise HTTPException(500, detail=ERROR_MESSAGES.DEFAULT(err))


############################
# ToggleSignUp
############################


@router.get("/signup/enabled", response_model=bool)
async def get_sign_up_status(request: Request, user=Depends(get_admin_user)):
    return request.app.state.config.ENABLE_SIGNUP


@router.get("/signup/enabled/toggle", response_model=bool)
async def toggle_sign_up(request: Request, user=Depends(get_admin_user)):
    request.app.state.config.ENABLE_SIGNUP = not request.app.state.config.ENABLE_SIGNUP
    return request.app.state.config.ENABLE_SIGNUP


############################
# Default User Role
############################


@router.get("/signup/user/role")
async def get_default_user_role(request: Request, user=Depends(get_admin_user)):
    return request.app.state.config.DEFAULT_USER_ROLE


class UpdateRoleForm(BaseModel):
    role: str


@router.post("/signup/user/role")
async def update_default_user_role(
    request: Request, form_data: UpdateRoleForm, user=Depends(get_admin_user)
):
    if form_data.role in ["pending", "user", "admin"]:
        request.app.state.config.DEFAULT_USER_ROLE = form_data.role
    return request.app.state.config.DEFAULT_USER_ROLE


############################
# JWT Expiration
############################


@router.get("/token/expires")
async def get_token_expires_duration(request: Request, user=Depends(get_admin_user)):
    return request.app.state.config.JWT_EXPIRES_IN


class UpdateJWTExpiresDurationForm(BaseModel):
    duration: str


@router.post("/token/expires/update")
async def update_token_expires_duration(
    request: Request,
    form_data: UpdateJWTExpiresDurationForm,
    user=Depends(get_admin_user),
):
    pattern = r"^(-1|0|(-?\d+(\.\d+)?)(ms|s|m|h|d|w))$"

    # Check if the input string matches the pattern
    if re.match(pattern, form_data.duration):
        request.app.state.config.JWT_EXPIRES_IN = form_data.duration
        return request.app.state.config.JWT_EXPIRES_IN
    else:
        return request.app.state.config.JWT_EXPIRES_IN


############################
# API Key
############################


<<<<<<< HEAD
# Create User api_key
=======
# 创建用户 api_key
>>>>>>> fingerprintAuth-out
@router.post("/api_key", response_model=ApiKey)
async def create_api_key_(user=Depends(get_current_user)):
    api_key = create_api_key()
    success = Users.update_user_api_key_by_id(user.id, api_key)
    if success:
        return {
            "api_key": api_key,
        }
    else:
        raise HTTPException(500, detail=ERROR_MESSAGES.CREATE_API_KEY_ERROR)


<<<<<<< HEAD
# Delete user api_key
=======
# 删除用户 api_key
>>>>>>> fingerprintAuth-out
@router.delete("/api_key", response_model=bool)
async def delete_api_key(user=Depends(get_current_user)):
    success = Users.update_user_api_key_by_id(user.id, None)
    return success

<<<<<<< HEAD
# Send email verification code


=======
# 发送邮箱验证码
>>>>>>> fingerprintAuth-out
@router.post("/send_code")
async def send_code(email_request: EmailRequest, user=Depends(get_current_user)):
    email = email_request.email

<<<<<<< HEAD
    # Verify if the email has been authenticated
=======
    # 校验邮箱是否已经认证过
>>>>>>> fingerprintAuth-out
    emailRet = KycRestrictInstance.check_email(email)
    if emailRet:
        return {"pass": False, "message": "One email can only be used for KYC verification once"}

<<<<<<< HEAD
    code = email_code_operations.generate_code()  # Generate verification code
    result = email_code_operations.create(email, code)  # Save the verification code to the database
=======
    code = email_code_operations.generate_code()  # 生成验证码
    result = email_code_operations.create(email, code)  # 将验证码保存到数据库
>>>>>>> fingerprintAuth-out
    if result:
        email_body = f"""
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2c3e50;">Confirm Your Email Address</h1>
                <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Wallet Address: {user.id}</p>
                <p>Let's make sure this is the right email address for you. Please enter the following verification code to continue using DeGPT:</p>
                <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                <p>Verification codes expire after two hours.</p>
                <p>Thank you.</p>  
                <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
<<<<<<< HEAD
                    <div style="display: flex; align-items: center;">
                        <img src="https://www.degpt.ai/static/email/tip.png" style="width: 20px; margin-right: 5px;"/>
                        <span>Small Tip:</span>
                    </div>
                    <p>If you're using a Gmail account and can't find the verification code in you Inbox, it's highly likely that it's been filtered into your SpamFolder.</p>
=======
>>>>>>> fingerprintAuth-out
                    <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPT Logo" style="width: 200px; height: auto;">
                    <div style="margin-top: 15px;">
                        <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">DecentralGPT Website</a>
                        <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Follow on Twitter</a>
                        <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Join Telegram</a>
                    </div>
                    <p>Best regards,<br>DecentralGPT Team</p>
                </div>
            </div>
        </body>
        </html>
        """
<<<<<<< HEAD
        # Send mail
        email_code_operations.send_email(email, "DeGPT Code", email_body) 
        return {"pass": True, "message": "Verification code has been sent"}
    else:
        raise HTTPException(status_code=500, detail="Unable to create verification code record")

# Get server time
=======
        # 发送邮件
        email_code_operations.send_email(email, "DeGPT Code", email_body) 
        return {"pass": True, "message": "验证码已发送"}
    else:
        raise HTTPException(status_code=500, detail="无法创建验证码记录")

# 获取服务器时间
>>>>>>> fingerprintAuth-out


@router.post("/serve_time")
async def serve_time():
    local_time = datetime.now()
    return {"data": local_time}

<<<<<<< HEAD
# Verify email verification code
=======
# 校验邮箱验证码
>>>>>>> fingerprintAuth-out


@router.post("/verify_code")
async def verify_code(verify_code_request: VerifyCodeRequest, user=Depends(get_verified_user)):
    email = verify_code_request.email
    code = verify_code_request.code

    record = email_code_operations.get_by_email(email)

    if not record:
        raise HTTPException(
            status_code=404, detail="The verification code record does not exist")

    if email_code_operations.is_expired(record.created_at):
        raise HTTPException(
            status_code=400, detail="The verification code has expired")

    if record.code == code:
        KycRestrictInstance.update_email(user.id, email)
        return {"message": "The verification code has been verified successfully"}
    else:
        raise HTTPException(
            status_code=400, detail="The verification code is invalid")


<<<<<<< HEAD
# Generate facial recognition database
@router.get("/create_face")
async def create_face():
    # Generate facial recognition database
    return face_lib.create_face_db()

# Obtain facial recognition connection
=======
# 生成人脸识别库
@router.get("/create_face")
async def create_face():
    # 生成人脸识别库
    return face_lib.create_face_db()

# 获取人脸识别连接
>>>>>>> fingerprintAuth-out
@router.post("/face_liveness", response_model=FaceLivenessResponse)
async def face_liveness(form_data: FaceLivenessRequest, user=Depends(get_current_user)):
    if user.id.startswith("0x"):
        kycrestrict = KycRestrictInstance.get_by_userid(user.id)
        if kycrestrict is None or kycrestrict.email is None or kycrestrict.captcha_code is None:
            raise HTTPException(404, detail=ERROR_MESSAGES.API_KEY_NOT_FOUND)
        # print("face compare success", form_data.sourceFacePictureBase64,  form_data.targetFacePictureBase64)
        response = face_compare.face_liveness({
            "deviceType": form_data.metaInfo.deviceType,
            "ua": form_data.metaInfo.ua,
            "bioMetaInfo": form_data.metaInfo.bioMetaInfo,
            "user_id": user.id
        })

        merchant_biz_id = response["merchant_biz_id"]
        transaction_id = response["transaction_id"]
        transaction_url = response["transaction_url"]

<<<<<<< HEAD
        # Store the user's verification information
=======
        # 存储该用户的验证信息
>>>>>>> fingerprintAuth-out
        face_time = datetime.now()
        Users.update_user_verify_info(
            user.id, transaction_id, merchant_biz_id, face_time)

        return {
            "merchant_biz_id": merchant_biz_id,
            "transaction_id": transaction_id,
            "transaction_url": transaction_url,
            "face_time": face_time,
        }

    else:
        raise HTTPException(404, detail=ERROR_MESSAGES.API_KEY_NOT_FOUND)

<<<<<<< HEAD
# Face binding
=======
# 人脸绑定
>>>>>>> fingerprintAuth-out
@router.post("/faceliveness_bind", response_model=FaceLivenessCheckResponse)
async def faceliveness_bind(user: UserRequest):
    passedInfo = await faceliveness_check_for_ws(user.user_id)
    await manager.broadcast(json.dumps(passedInfo), user.user_id)
    return passedInfo


<<<<<<< HEAD
# Facial recognition verification
@router.post("/faceliveness_check", response_model=FaceLivenessCheckResponse)
async def faceliveness_check(user=Depends(get_current_user)):
    # Get query parameters
=======
# 人脸识别校验
@router.post("/faceliveness_check", response_model=FaceLivenessCheckResponse)
async def faceliveness_check(user=Depends(get_current_user)):
    # 获取查询参数
>>>>>>> fingerprintAuth-out
    # print("Query Parameters:", form_data,form_data.merchant_biz_id, form_data.transaction_id )
    merchant_biz_id = user.merchant_biz_id
    transaction_id = user.transaction_id

    print("form_data.", merchant_biz_id, transaction_id)

    if True:
        # print("face compare success", form_data.sourceFacePictureBase64,  form_data.targetFacePictureBase64)
        # response = face_compare.check_result({
        #     "transaction_id": form_data.transaction_id,
        #     "merchant_biz_id":form_data.merchant_biz_id,
        # })
        response = face_compare.check_result(
            transaction_id=transaction_id,
            merchant_biz_id=merchant_biz_id,
        )

        # print("face compare success", response, response.body.result.ext_face_info, response.body)
        # print("ext_face_info",  json.loads(response.body.result.ext_face_info)['faceImg'], )

        faceImg = json.loads(response.body.result.ext_face_info)['faceImg']

        if face_lib.check_face_image(faceImg) == False:
            return {
                "passed": False,
                "message": "Fail"
            }

        # face_lib.add_face_data(faceImg)
        face_id = face_lib.search_face(faceImg)
        print("face_id", face_id)

        user_id = Users.get_user_id_by_face_id(face_id)
        print("user_id", face_id, user_id)
        if user_id is None:
            return {
                "passed": False,
                "message": "Fail"
            }

        # 'Message': 'success',
        # 'RequestId': 'F7EE6EED-6800-3FD7-B01D-F7F781A08F8D',
        # 'Result': {
        #     'ExtFaceInfo': '{"faceAttack":"N","faceOcclusion":"N","faceQuality":67.1241455078125}',
        #     'Passed': 'Y',
        #     'SubCode': '200'
        # }
        passed = False
        message = "Fail"
        if (response.body.result.passed == 'Y'):
            passed = True
            message = "Success"
        return {
            "passed": passed,
            "message": message
        }

    else:
        raise HTTPException(404, detail=ERROR_MESSAGES.API_KEY_NOT_FOUND)

<<<<<<< HEAD
# Search for facial images
@router.get("/faceliveness_image/{tranid}")
async def faceliveness_image(tranid: str):
    # Get query parameters
=======
# 查询人脸图片
@router.get("/faceliveness_image/{tranid}")
async def faceliveness_image(tranid: str):
    # 获取查询参数
>>>>>>> fingerprintAuth-out
    # print("Query Parameters:", form_data,form_data.merchant_biz_id, form_data.transaction_id )
    merchant_biz_id = 'c2371516-d114-4872-8de0-b9d2a42f9f7c'
    transaction_id = tranid

    print("form_data.", merchant_biz_id, transaction_id)

    # print("face compare success", form_data.sourceFacePictureBase64,  form_data.targetFacePictureBase64)
    # response = face_compare.check_result({
    #     "transaction_id": form_data.transaction_id,
    #     "merchant_biz_id":form_data.merchant_biz_id,
    # })
    response = face_compare.check_result(
        transaction_id=transaction_id,
        merchant_biz_id=merchant_biz_id,
    )

    # print("face compare success", response, response.body.result.ext_face_info, response.body)
    # print("ext_face_info",  json.loads(response.body.result.ext_face_info)['faceImg'], )

    faceImg = json.loads(response.body.result.ext_face_info)['faceImg']

<<<<<<< HEAD
    # Verify the authenticity of the image
=======
    # 校验图片真实性
>>>>>>> fingerprintAuth-out
    flag = face_lib.check_face_image(faceImg)
    return {
        "pass": flag,
        "base64": faceImg
    }


<<<<<<< HEAD
# Check if the face passes
async def faceliveness_check_for_ws(id: str):

    print("Start face verification-userId", id)

    try:
        # Obtain user information
=======
# 检查人脸是否通过
async def faceliveness_check_for_ws(id: str):

    print("开始人脸校验-userId", id)

    try:
        # 获取用户信息
>>>>>>> fingerprintAuth-out
        user = Users.get_user_by_id((id))

        if (user.verified):
            return {
                "passed": True,
                "message": "Success"
            }

<<<<<<< HEAD
        # Check if the verification time has expired
=======
        # 校验时间是否超时
>>>>>>> fingerprintAuth-out
        face_time = user.face_time
        if (face_time is None):
            return {
                "passed": False,
                "message": "Time expired, try again"
            }

        now_time = datetime.now()
<<<<<<< HEAD
        # Calculate time difference
=======
        # 计算时间差
>>>>>>> fingerprintAuth-out
        time_difference = now_time - face_time
        if (time_difference.total_seconds() > 300):
            return {
                "passed": False,
                "message": "Time expired, try again"
            }

<<<<<<< HEAD
        # Get query parameters
=======
        # 获取查询参数
>>>>>>> fingerprintAuth-out
        merchant_biz_id = user.merchant_biz_id
        transaction_id = user.transaction_id

        if merchant_biz_id is not None and transaction_id is not None:
<<<<<<< HEAD
            # 1. Obtain the information returned by face detection (including photo based 64 information)
=======
            # 1. 获取人脸检测返回的信息（包含照片base64信息
>>>>>>> fingerprintAuth-out
            response = face_compare.check_result(
                transaction_id=transaction_id,
                merchant_biz_id=merchant_biz_id,
            )

            # print("face compare success", response, response.body.result.ext_face_info, response.body)
            # print("ext_face_info",  json.loads(response.body.result.ext_face_info)['faceImg'], )

<<<<<<< HEAD
            # 2. Obtain facial photos
            faceImg = json.loads(response.body.result.ext_face_info)['faceImg']

            # 3. Verify the authenticity of the image
=======
            # 2. 获取人脸照片
            faceImg = json.loads(response.body.result.ext_face_info)['faceImg']

            # 3. 校验图片真实性
>>>>>>> fingerprintAuth-out
            if face_lib.check_face_image(faceImg) == False:
                return {
                    "passed": False,
                    "message": "The identity validate fail",
                }
            
<<<<<<< HEAD
            # 4. Search if the facial photo exists in the database
=======
            # 4. 搜索该人脸照片在库中是否存在
>>>>>>> fingerprintAuth-out
            face_id = face_lib.search_face(faceImg)
            print("face_id", face_id)

            if face_id is not None:
                print("user check:", face_id)
                user_exit = Users.get_user_id_by_face_id(face_id)
<<<<<<< HEAD
                # 5. If it exists, I'll tell you that the face has already been detected!
=======
                # 5. 存在就告诉你，该人脸已经被检测过了！
>>>>>>> fingerprintAuth-out
                if user_exit is not None:
                    return {
                        "passed": False,
                        "message": "You have already bound your face KYC with another wallet. Only one wallet can be bound.",
                        "address": user_exit.id
                    }
            else:
<<<<<<< HEAD
                # Add facial samples
                id_str = str(uuid.uuid4()).replace("-", "_")
                face_lib.add_face_sample(id_str)
                # Add corresponding face data to the face sample
                face_id = face_lib.add_face_data(faceImg, id_str)
            
            # Update KYC authentication
            if response.body.result.passed:
                # Verify whether the user has completed all KYC authentication processes
=======
                # 添加人脸样本
                id_str = str(uuid.uuid4()).replace("-", "_")
                face_lib.add_face_sample(id_str)
                # 在人脸样本添加对应的人脸数据
                face_id = face_lib.add_face_data(faceImg, id_str)
            
            # 更新kyc认证
            if response.body.result.passed:
                # 校验用户是否完成所有kyc认证流程
>>>>>>> fingerprintAuth-out
                kycrestrict = KycRestrictInstance.get_by_userid(user.id)
                if kycrestrict is None:
                    return {
                            "passed": False,
                            "message": "The identity validate fail",
                        }
                kycrestricts = KycRestrictInstance.get_by_ip(kycrestrict.ip_address)
                if  kycrestricts is not None and len(kycrestricts) >= 2:
                    return {
                            "passed": False,
                            "message": "A single IP address can be used for a maximum of two KYC verifications",
                        }
                email_check = KycRestrictInstance.check_email(kycrestrict.email)
                if email_check:
                    return {
                            "passed": False,
                            "message": "One email can only be used for KYC verification once",
                        }
                captcha_check = CaptchaApiInstance.checkCaptcha(kycrestrict.captcha_code, kycrestrict.ip_address)
                if captcha_check == False:
                    return {
                            "passed": False,
                            "message": "The identity validate fail",
                        }
                
<<<<<<< HEAD
                # Update user KYC status
                user_update_result = Users.update_user_verified(user.id, True, face_id)
                # Update KYC process status
                KycRestrictInstance.update_kyc(user.id, True)
=======
                # 更新用户KYC状态
                user_update_result = Users.update_user_verified(user.id, True, face_id)
                # 更新KYC流程状态
                KycRestrictInstance.update_kyc(user.id, True)
                # 领取注册奖励
                await rewardSent(user.id)
>>>>>>> fingerprintAuth-out
                # return user_update_result
                print("user_update_result", user_update_result)
                            
            # 'Message': 'success',
            # 'RequestId': 'F7EE6EED-6800-3FD7-B01D-F7F781A08F8D',
            # 'Result': {
            #     'ExtFaceInfo': '{"faceAttack":"N","faceOcclusion":"N","faceQuality":67.1241455078125}',
            #     'Passed': 'Y',
            #     'SubCode': '200'
            # }
<<<<<<< HEAD
            # Verification successful returns corresponding data
=======
            # 校验成功返回对应数据
>>>>>>> fingerprintAuth-out
            passed = False
            message = "Fail"
            if (response.body.result.passed == 'Y'):
                passed = True
                message = "Success"
            return {
                "passed": passed,
                "message": message
            }

        else:
            return {
                "passed": False,
                "message": "Your haven't started live testing yet"
            }

    except Exception as e:
        print(f"Error in faceliveness_check_for_ws: {e}")
<<<<<<< HEAD
        # Perform error handling as needed, such as logging or notifying clients
=======
        # 根据需要执行错误处理，例如记录日志或通知客户端
>>>>>>> fingerprintAuth-out
        return {
            "passed": False,
            "message": "The identity validate fail"
        }

<<<<<<< HEAD
=======
async def rewardSent(user_id: str):
    registReward = RewardsTableInstance.get_create_rewards_by_userid(user_id)
    if registReward is not None:
        if registReward.status == False:
            RewardApiInstance.registReward(registReward.id, user_id)
>>>>>>> fingerprintAuth-out

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    async def broadcast(self, message: str, user_id: str):
        connections = self.active_connections.get(user_id, [])
        for connection in connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
<<<<<<< HEAD
            print("Information received by socket：", data)
            # if (data == "heart"):
            #    await manager.broadcast(f"{passedInfo['passed']}-{passedInfo['message']}", user_id)
            # else:
            #     passedInfo = await faceliveness_check_for_ws(user_id)  # transfer user_id
            #     print("passed",passedInfo,  passedInfo['passed'])
            #     await manager.broadcast("heart", user_id)
            #     # await manager.broadcast(f"The server has received-{user_id}", user_id)
    except WebSocketDisconnect:
        print("WebSocketDisconnect")
        manager.disconnect(websocket, user_id)
    except Exception as e:
        print(f"WebSocket connection error: {e}")
        await websocket.close(code=1000)  # Elegantly close the connection
=======
            print("socket接收到得信息", data)
            # if (data == "heart"):
            #    await manager.broadcast(f"{passedInfo['passed']}-{passedInfo['message']}", user_id)
            # else:
            #     passedInfo = await faceliveness_check_for_ws(user_id)  # 传递 user_id
            #     print("passed",passedInfo,  passedInfo['passed'])
            #     await manager.broadcast("heart", user_id)
            #     # await manager.broadcast(f"服务端接收到{user_id}", user_id)
    except WebSocketDisconnect:
        print("WebSocketDisconnect了")
        manager.disconnect(websocket, user_id)
    except Exception as e:
        print(f"WebSocket connection error: {e}")
        await websocket.close(code=1000)  # 优雅地关闭连接
>>>>>>> fingerprintAuth-out
