from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends

from apps.web.models.users import Users

from pydantic import BaseModel
from typing import Union, Optional
from constants import ERROR_MESSAGES
from passlib.context import CryptContext
from datetime import datetime, timedelta
import requests
import jwt
import uuid
import logging
import config

logging.getLogger("passlib").setLevel(logging.ERROR)


SESSION_SECRET = config.WEBUI_SECRET_KEY
ALGORITHM = "HS256"

##############
# Auth Utils
##############

bearer_security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return (
        pwd_context.verify(plain_password, hashed_password) if hashed_password else None
    )


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    生成JWT Token
    
    Args:
        data (dict): 包含JWT负载信息的字典
        expires_delta (Union[timedelta, None], optional): Token过期时间差，默认为None。
    
    Returns:
        str: 生成的JWT Token字符串
    
    """
    # 复制传入的字典数据
    payload = data.copy()

    # 如果传入了过期时间差
    if expires_delta:
        # 计算过期时间
        expire = datetime.utcnow() + expires_delta
        # 将过期时间加入到payload中
        payload.update({"exp": expire})

    # 使用jwt库对payload进行编码生成JWT
    encoded_jwt = jwt.encode(payload, SESSION_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    try:
        decoded = jwt.decode(token, SESSION_SECRET, algorithms=[ALGORITHM])
        return decoded
    except Exception as e:
        return None


def extract_token_from_auth_header(auth_header: str):
    return auth_header[len("Bearer ") :]


def create_api_key():
    key = str(uuid.uuid4()).replace("-", "")
    return f"sk-{key}"


def get_http_authorization_cred(auth_header: str):
    try:
        scheme, credentials = auth_header.split(" ")
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
    except:
        raise ValueError(ERROR_MESSAGES.INVALID_TOKEN)


def get_current_user(
    # 传入HTTPAuthorizationCredentials类型的auth_token参数，默认为Depends(bearer_security)
    auth_token: HTTPAuthorizationCredentials = Depends(bearer_security),
):
    print("auth_token", auth_token)

    # 根据API密钥进行认证
    # auth by api key
    if auth_token.credentials.startswith("sk-"):
        # 调用get_current_user_by_api_key函数，传入auth_token.credentials作为参数，返回当前用户
        return get_current_user_by_api_key(auth_token.credentials)

    # 解码token
    # auth by jwt token
    data = decode_token(auth_token.credentials)

    # 如果解码后的数据不为空且包含"id"字段
    if data != None and "id" in data:
        # 根据id获取用户
        user = Users.get_user_by_id(data["id"])

        # 如果用户不存在
        if user is None:
            # 抛出HTTP异常，状态码为401，错误详情为无效的token
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ERROR_MESSAGES.INVALID_TOKEN,
            )
        else:
            # 更新用户的最后活跃时间
            Users.update_user_last_active_by_id(user.id)

        # 返回当前用户
        return user

    else:
        # 抛出HTTP异常，状态码为401，错误详情为未授权
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )


def get_current_user_by_api_key(api_key: str):
    user = Users.get_user_by_api_key(api_key)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.INVALID_TOKEN,
        )
    else:
        Users.update_user_last_active_by_id(user.id)

    return user


def get_verified_user(user=Depends(get_current_user)):
    if user.role not in {"user", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )
    return user


def get_admin_user(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )
    return user
