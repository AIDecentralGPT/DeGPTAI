from fastapi import APIRouter, Depends, HTTPException
from apps.web.models.ip_log import IpLog
from apps.web.models.users  import User
from utils.utils import get_verified_user

router = APIRouter()

# 添加IP记录
@router.post("/ip_logs")
async def add_ip_log(user_id: str, ip_address: str, user=Depends(get_verified_user)):
    try:
        existing_ip_log = IpLog.get(IpLog.ip_address == ip_address)
        return {"message": "IP address already used for rewards."}
    except IpLog.DoesNotExist:
        user = User.get(User.id == user_id)
        IpLog.create(user=user, ip_address=ip_address)
        return {"message": "IP address logged successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
