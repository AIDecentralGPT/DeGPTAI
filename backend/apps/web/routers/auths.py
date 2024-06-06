import logging

from fastapi import Request, UploadFile, File
from fastapi import Depends, HTTPException, status

from fastapi import APIRouter
from pydantic import BaseModel
import re
import uuid
import csv
from apps.web.models.chats import (
    ChatModel,
    ChatResponse,
    ChatTitleForm,
    ChatForm,
    ChatTitleIdResponse,
    Chats,
)


# --------钱包相关--------
from substrateinterface import Keypair, KeypairType
from substrateinterface.utils.ss58 import ss58_decode
from substrateinterface.utils.hasher import blake2_256
import json

# https://chatgpt.com/c/ea2b63e6-234f-45ad-8e32-a338f3c76737




# # 假设前端传递的数据格式如下：
# data = {
#     "address": "5FHneW46xGXgs5mUiveU4sbTyGBzmtoZygMnNrpHRT7Pu8oB",
#     "nonce": "some-random-nonce",
#     "message": "The message to be signed",
#     "signature": "0x38d5724ace9f5fbd..."
# }







# ————————————————————————


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
    
)
from apps.web.models.users import Users
from apps.web.models.visitors import visitors_table

from utils.utils import (
    get_password_hash,
    get_current_user,
    get_admin_user,
    create_token,
    create_api_key,
)
from utils.misc import parse_duration, validate_email_format
from utils.webhook import post_webhook
from constants import ERROR_MESSAGES, WEBHOOK_MESSAGES
from config import WEBUI_AUTH, WEBUI_AUTH_TRUSTED_EMAIL_HEADER

router = APIRouter()

############################
# GetSessionUser
############################


@router.get("/", response_model=UserResponse)
async def get_session_user(user=Depends(get_current_user)):
    # print("get_session_user 的 user:" , user.id, user)
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "profile_image_url": user.profile_image_url,
    }
    # print("get_session_user 的 user:" , user['id'], user)
    # return {
    #     "id": user['id'],
    #     "email": user['email'],
    #     "name": user.name,
    #     "role": user.role,
    #     "profile_image_url": user.profile_image_url,
    # }



############################
# Update Profile
############################


@router.post("/update/profile", response_model=UserResponse)
async def update_profile(
    form_data: UpdateProfileForm, session_user=Depends(get_current_user)
):
    if session_user:
        try:
            user = Users.update_user_by_id(
                session_user.id,
                {"profile_image_url": form_data.profile_image_url, "name": form_data.name},
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


# ############################
# # printSignIn(根据指纹身份校验)
# ############################
# # @router.post("/fingerprintSignIn", response_model=FingerprintSigninResponse)
# @router.post("/fingerprintSignIn", response_model=None)
# async def printSignIn(request: Request, form_data: FingerprintSignInForm):
#     # 生成UUID并转换为字符串
#     id_str = str(uuid.uuid4())
#     visitors_table.insert_new_visitor(id_str, form_data.visitor_id)

#     #  # 检查用户是否存在，如果不存在则进行注册
#     # if not Users.get_user_by_email(trusted_email.lower()):
#     #     await signup(
#     #         request,
#     #         SignupForm(
#     #             email=trusted_email, password=str(uuid.uuid4()), name=trusted_email
#     #         ),
#     #     )



    # # 检查是否启用了基于信任头的 WebUI 认证
    # if WEBUI_AUTH_TRUSTED_EMAIL_HEADER:
    #     print("检查是否启用了基于信任头的 WebUI 认证")

    #     # 检查用户是否存在，如果不存在则进行注册
    #     if not Users.get_user_by_email(trusted_email.lower()):
    #         await signup(
    #             request,
    #             SignupForm(
    #                 email=trusted_email, password=str(uuid.uuid4()), name=trusted_email
    #             ),
    #         )



    #     print("检查是否禁用了 WebUI 认证")
    #     admin_email = "admin@localhost"
    #     admin_password = "admin"
    #     print(2)

    #     # 检查管理员账号是否存在
    #     if Users.get_user_by_email(admin_email.lower()):
    #         # 管理员账号存在，进行认证
    #         user = Auths.authenticate_user(admin_email.lower(), admin_password)
    #     else:
    #         # 管理员账号不存在，检查是否有其他用户
    #         if Users.get_num_users() != 0:
    #             raise HTTPException(400, detail=ERROR_MESSAGES.EXISTING_USERS)

    #         # 没有其他用户，进行管理员账号注册
    #         await signup(
    #             request,
    #             SignupForm(email=admin_email, password=admin_password, name="User"),
    #         )

    #         # 注册完成后，再次进行认证
    #         user = Auths.authenticate_user(admin_email.lower(), admin_password)
    # else:
    #     # 使用表单中的邮箱和密码进行用户认证
    #     user = Auths.authenticate_user(form_data.email.lower(), form_data.password)
    #     print("使用表单中的邮箱和密码进行用户认证", user)

    # # 如果认证成功，则生成令牌并返回用户信息
    # if user:
    #     token = create_token(
    #         data={"id": user.id},
    #         expires_delta=parse_duration(request.app.state.config.JWT_EXPIRES_IN),
    #     )

    #     return {
    #         "token": token,
    #         "token_type": "Bearer",
    #         "id": user.id,
    #         "email": user.email,
    #         "name": user.name,
    #         "role": user.role,
    #         "profile_image_url": user.profile_image_url,
    #     }
    # else:
    #     # 如果认证失败，则打印日志并返回错误提示
    #     print(3)
    #     raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)




############################
# SignIn
############################

@router.post("/printSignIn", response_model=None)
async def printSignIn(request: Request, form_data: FingerprintSignInForm):
    print("Received printSignIn request")  # 打印日志
    try:
        user = Users.get_user_by_id(form_data.id)
    except Exception as e:
        print("Error retrieving user by id:", e.message)

    if user:
        print("User found:", user.id)
    else:
        print("User not found, creating new user")
        hashed = get_password_hash("")
        Auths.insert_new_auth(
            "",
            hashed,
            "visitor",
            "data:image/jpeg;base64,...",
            "user",
            form_data.id,
        )
        print("Auths.insert_new_auth执行完毕")

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
    }
    # print("Returning response:", response)  # 打印日志
    return response






# 钱包登录，校验钱包数据(可以用，就是结果是false)
# https://polkascan.github.io/py-substrate-interface/usage/keypair-creation-and-signing/?h=verify#verify-generated-signature-with-public-address
@router.post("/walletSignIn")
async def walletSignIn(request: Request, form_data: WalletSigninForm):
    print("Received Data:", form_data)
    
    address = form_data.address
    nonce = form_data.nonce
    signature_hex = form_data.signature
    try:

        # 检查并去除0x前缀
        if signature_hex.startswith("0x"):
            signature_hex = signature_hex[2:]

        # 验证签名格式
        if not re.fullmatch(r'[0-9a-fA-F]+', signature_hex):
            raise HTTPException(status_code=400, detail="Invalid signature format")

        print("form_data", address, nonce, signature_hex)

        # 将签名从十六进制转换为字节
        signature = bytes.fromhex(signature_hex)


        # 创建Keypair对象
        keypair_public = Keypair(ss58_address=address, crypto_type=KeypairType.SR25519)
        is_valid = keypair_public.verify(nonce, signature)

        if is_valid:
            # 创建新的用户，id为address。（后面可以考虑把指纹登录的用户给删除）
            user = Users.get_user_by_id(form_data.address)




            if user:
                # 这里先不做事情，后面会返回用户
                print("User found:", user.id)

                

            else:
                # 删除所有聊天记录
                result = Chats.delete_chats_by_user_id(user.id)
                print("删除所有聊天记录", result)   
                # 创建新用户，用钱包地址作为id
                print("User not found, creating new user")
                hashed = get_password_hash("")
                Auths.insert_new_auth(
                    "",
                    hashed,
                    "visitor",
                    "data:image/jpeg;base64,...",
                    "user",
                    form_data.address,
                )
                print("Auths.insert_new_auth执行完毕")

                user = Users.get_user_by_id(form_data.id)
                print("New user created:", user.id, user)
    
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
            }
            return response


        # #   更新表格的name为address
        #     id = form_data.id
        #     updated_user = Users.update_user_by_id(
        #         id,
        #         {
        #             "name": form_data.address,
        #         },
        #     )
        #     print("updated_user", updated_user)

        #     return {
        #             "is_valid": is_valid,
        #             "userData": updated_user
        #         }

        else :
            raise HTTPException(status_code=400, detail="Sign is error")



        # return {
        #     "is_valid": is_valid
        # }

    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



# @router.post("/walletSignIn", response_model=None)
# async def walletSignIn(request: Request, form_data: FingerprintSignInForm):
#     print("walletSignIn执行")
#     try:
#         user  = Users.get_user_by_id(form_data.id)
#     except Exception as e:
#         print("Users.get_user_by_id(form_data.id)", e.message)

#     if user:
#         # print("有此访客", user, user.id)
#         print("有此访客", )
#         # Auths.update_user_id(user.id, form_data.id)


#     else: 
#         print(222)
#         hashed = get_password_hash("")
#         print("无此访客，创建新访客", form_data.id)
#         # token = create_token(
#         #     data={"id": user.id},
#         #     expires_delta=parse_duration(request.app.state.config.JWT_EXPIRES_IN),
#         #               )
#         Auths.insert_new_auth(
#             "",
#             hashed,
#             "visitor",
#             "data:image/jpeg;base64,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",
#             "user",
#             form_data.id,
#             # "token": token,
#         )
        

#         user = Users.get_user_by_id(form_data.id)
    
#     token = create_token(
#             data={"id": user.id},
#             expires_delta=parse_duration(request.app.state.config.JWT_EXPIRES_IN),
#     )
#     # return {
#     #     token,
#     #       "token_type": "Bearer",
#     #         "id": user.id,
#     #         "email": user.email,
#     #         "name": user.name,
#     #         "role": user.role,
#     #         "profile_image_url": user.profile_image_url,
#     # }
#     return {
#         "token": token,
#         "token_type": "Bearer",
#         "id": user.id,
#         "email": user.email,
#         "name": user.name,
#         "role": user.role,
#         "profile_image_url": user.profile_image_url,
#     }




@router.post("/signin", response_model=SigninResponse)
async def signin(request: Request, form_data: SigninForm):
    # 检查是否启用了基于信任头的 WebUI 认证
    if WEBUI_AUTH_TRUSTED_EMAIL_HEADER:
        print("检查是否启用了基于信任头的 WebUI 认证")
        # 检查请求头中是否包含信任头
        if WEBUI_AUTH_TRUSTED_EMAIL_HEADER not in request.headers:
            print(1)
            raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_TRUSTED_HEADER)

        # 获取信任头中的邮箱并转为小写
        trusted_email = request.headers[WEBUI_AUTH_TRUSTED_EMAIL_HEADER].lower()
        # 检查用户是否存在，如果不存在则进行注册
        if not Users.get_user_by_email(trusted_email.lower()):
            await signup(
                request,
                SignupForm(
                    email=trusted_email, password=str(uuid.uuid4()), name=trusted_email
                ),
            )

        # 通过信任头邮箱进行用户认证
        user = Auths.authenticate_user_by_trusted_header(trusted_email)
    # 检查是否禁用了 WebUI 认证
    elif WEBUI_AUTH == False:
        print("检查是否禁用了 WebUI 认证")
        admin_email = "admin@localhost"
        admin_password = "admin"
        print(2)

        # 检查管理员账号是否存在
        if Users.get_user_by_email(admin_email.lower()):
            # 管理员账号存在，进行认证
            user = Auths.authenticate_user(admin_email.lower(), admin_password)
        else:
            # 管理员账号不存在，检查是否有其他用户
            if Users.get_num_users() != 0:
                raise HTTPException(400, detail=ERROR_MESSAGES.EXISTING_USERS)

            # 没有其他用户，进行管理员账号注册
            await signup(
                request,
                SignupForm(email=admin_email, password=admin_password, name="User", visiter_id = form_data.visiter_id),
            )

            # 注册完成后，再次进行认证
            user = Auths.authenticate_user(admin_email.lower(), admin_password, )
    else:
        # 使用表单中的邮箱和密码进行用户认证
        user = Auths.authenticate_user(form_data.email.lower(), form_data.password)
        print("使用表单中的邮箱和密码进行用户认证", user)

    # 如果认证成功，则生成令牌并返回用户信息
    if user:
        token = create_token(
            data={"id": user.id},
            expires_delta=parse_duration(request.app.state.config.JWT_EXPIRES_IN),
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
        # 如果认证失败，则打印日志并返回错误提示
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
            form_data.id
        )

        if user:
            token = create_token(
                data={"id": user.id},
                expires_delta=parse_duration(request.app.state.config.JWT_EXPIRES_IN),
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


# create api key
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


# delete api key
@router.delete("/api_key", response_model=bool)
async def delete_api_key(user=Depends(get_current_user)):
    success = Users.update_user_api_key_by_id(user.id, None)
    return success


# get api key
@router.get("/api_key", response_model=ApiKey)
async def get_api_key(user=Depends(get_current_user)):
    api_key = Users.get_user_api_key_by_id(user.id)
    if api_key:
        return {
            "api_key": api_key,
        }
    else:
        raise HTTPException(404, detail=ERROR_MESSAGES.API_KEY_NOT_FOUND)
