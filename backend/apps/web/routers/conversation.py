from fastapi import APIRouter
from fastapi import Response, Request
from fastapi import Depends, FastAPI, HTTPException, status

import logging
from constants import ERROR_MESSAGES
from config import SRC_LOG_LEVELS

from apps.web.models.conversation import ConversationInstance, ConversationRequest
from utils.utils import (get_current_user)
from datetime import date

from apps.web.models.models import ModelsInstance
from apps.web.models.model_limit import ModelLimitInstance
from apps.web.models.vipstatus import VIPStatuses



log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

# 更新用户聊天统计
@router.post("/refresh")
async def conversationRefresh(conversation_req: ConversationRequest, user=Depends(get_current_user)):
    try:
        # 获取用户当前VIP信息
        vipStatus = VIPStatuses.get_vip_status_by_user_id(user.id)

        # 获取当前请求模型信息
        models = ModelsInstance.get_info_by_models(conversation_req.models)

        # 获取今天的聊天次数
        date_time = date.today()
        type_list = [model["type"] for model in models]
        conversations = ConversationInstance.get_info_by_userid_mtypes_date(user.id, type_list, date_time)

        # 判断用户类型
        userrole = "user"
        vip = 1
        if user.id.startswith("0x"):
            userrole = "wallet"
            if user.verified:
                userrole = "kyc"
            if vipStatus is not None:
                userrole = "all"
                vip = vipStatus.vip
        # 获取该角色请求模型的总次数
        modellimits = ModelLimitInstance.get_info_by_user_vip(userrole, vip)
                        
        result = []
        for model in conversation_req.models:
            modellimit = next((item for item in modellimits if item.model == model), None) if modellimits is not None else None
            conversation = next((item for item in conversations if item.model == model), None) if conversations is not None else None
            if modellimit is not None:
                if conversation is None: # 第一次请求模型直接添加
                    ConversationInstance.insert(user.id, model)
                else: # 已有数据进行更新
                    updateFlag = True
                    # 判断用户是否超出次数
                    if userrole == 'vip': # vip用户校验
                        if modellimit.vip <= conversation.chat_num:
                            updateFlag = False
                            result.append({
                                "passed": False,
                                "model": model,
                                "num": conversation.chat_num,
                                "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                            })
                    elif userrole == 'kyc': # kyc用户校验
                        if modellimit.kyc <= conversation.chat_num:
                            updateFlag = False
                            result.append({
                                "passed": False,
                                "model": model,
                                "num": conversation.chat_num,
                                "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                            })
                    elif userrole == 'wallet': # wallet用户校验
                        if modellimit.wallet <= conversation.chat_num:
                            updateFlag = False
                            result.append({
                                "passed": False,
                                "model": model,
                                "num": conversation.chat_num,
                                "message": "The number of attempts has exceeded the limit. Please complete KYC."
                            })
                    else:
                       if modellimit.normal <= conversation.chat_num:
                            updateFlag = False
                            result.append({
                                "passed": False,
                                "model": model,
                                "num": conversation.chat_num,
                                "message": "The number of attempts has exceeded the limit. Please create Wallet."
                            })
                    if updateFlag:
                        ConversationInstance.update(conversation)
        return {"passed": True, "data": result}
    except Exception as e:
        print("===========conversationRefresh==========", e)
        return {
            "passed": False,
            "message": "Failed"
        }

