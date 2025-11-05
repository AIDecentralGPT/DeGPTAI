from fastapi import Depends

from fastapi import APIRouter
import logging

from apps.web.models.apikey import ApiKeyTableInstance

from utils.utils import get_admin_user

from config import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

############################
# ApiKey
############################

@router.get("/list", response_model=dict)
async def get_apikeys(skip: int = 0, limit: int = 50, search: str = "", status: str = "", user=Depends(get_admin_user)):
    print("skip", skip, "limit", limit)
    return ApiKeyTableInstance.page(skip, limit, search, status)

@router.post("/add")
async def add_apikey(user=Depends(get_admin_user)):
    return ApiKeyTableInstance.insert()

@router.post("/{id}/status")
async def switch_status(id: str, user=Depends(get_admin_user)):
    return ApiKeyTableInstance.updateStatus(id)