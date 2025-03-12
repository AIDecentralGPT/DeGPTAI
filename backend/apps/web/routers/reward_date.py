from fastapi import Response, Request
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel
import logging

from apps.web.models.reward_data import RewardDateTableInstance, RewardDateModel, RewardDateRequest

from utils.utils import get_admin_user

from config import SRC_LOG_LEVELS


from utils.misc import parse_duration, validate_email_format




log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

############################
# RewardDate
############################

@router.get("/list", response_model=dict)
async def get_rewarddates(skip: int = 0, limit: int = 50, search: str = "", status: str = "", user=Depends(get_admin_user)):
    print("skip", skip, "limit", limit)
    return RewardDateTableInstance.page(skip, limit, search, status)


@router.post("/add")
async def add_rewarddate(rewarddate: RewardDateRequest, user=Depends(get_admin_user)):
    return RewardDateTableInstance.insert(rewarddate)

@router.post("/{id}/status")
async def switch_status(id: str, user=Depends(get_admin_user)):
    return RewardDateTableInstance.updateStatus(id)