from fastapi import APIRouter
from apps.web.api.mcpclient import McpInstall
from apps.web.models.mcpparam import McpParamReq

from fastapi import Depends
from utils.utils import (get_current_user)

router = APIRouter()

@router.post("/proxy")
async def mcp_proxy(param: McpParamReq, user=Depends(get_current_user)):
  result = McpInstall.get_address_overview(param.address)
  return result