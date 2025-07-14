from fastapi import APIRouter, Depends, HTTPException
from apps.web.models.device import Device

from apps.web.models.users  import User
from utils.utils import get_verified_user

router = APIRouter()

# 添加设备记录
@router.post("/devices")
async def add_device(user_id: str, device_id: str, user=Depends(get_verified_user)):
    try:
        user = User.get(User.id == user_id)
        existing_device = Device.get(Device.user == user, Device.device_id == device_id)
        return {"message": "Device already registered for this user."}
    except Device.DoesNotExist:
        Device.create(user=user, device_id=device_id)
        return {"message": "Device registered successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
