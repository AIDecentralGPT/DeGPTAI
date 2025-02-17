from fastapi import APIRouter
from fastapi import Response, Request
from fastapi import Depends, FastAPI, HTTPException, status

import logging
from constants import ERROR_MESSAGES
from config import SRC_LOG_LEVELS

from apps.web.models.conversation import ConversationInstance, ConversationRequest
from utils.utils import (get_current_user)
from datetime import date

from apps.web.models.model_limit import ModelLimitInstance
from apps.web.models.vip import VIPStatuses



log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

# 更新用户聊天统计
@router.post("/refresh")
async def conversationRefresh(conversation_req: ConversationRequest, user=Depends(get_current_user)):
    try:
        # 获取模型的聊天次数
        modellimits = ModelLimitInstance.get_info_by_models(conversation_req.models)

        # 获取今天的聊天次数
        date_time = date.today()
        conversations = ConversationInstance.get_info_by_userid_models_date(user.id, conversation_req.models, date_time)

        # 获取用户是否为vip用户
        vipflag = VIPStatuses.is_vip_active(user.id)
        result = []
        for model in conversation_req.models:
            modellimit = next((item for item in modellimits if item.model == model), None) if modellimits is not None else None
            conversation = next((item for item in conversations if item.model == model), None) if conversations is not None else None
            if modellimit is None:
                result.append({"passed": True, "model": model, "num": 0, "message": "ok"})
            else:
                if conversation is None:
                    ConversationInstance.insert(user.id, model)
                    result.append({"passed": True, "model": model, "num": 0, "message": "ok"})
                else:
                    # 判断用户是否超出次数
                    if vipflag:
                        if modellimit.vip <= conversation.chat_num:
                            result.append({
                                "passed": False,
                                "model": model,
                                "num": conversation.chat_num,
                                "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                            })
                    else:
                        if user.id.startswith("0x"):
                            if modellimit.wallet <= conversation.chat_num:
                                result.append({
                                    "passed": False,
                                    "model": model,
                                    "num": conversation.chat_num,
                                    "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                                })
                        else:
                            if modellimit.normal <= conversation.chat_num:
                                result.append({
                                    "passed": False,
                                    "model": model,
                                    "num": conversation.chat_num,
                                    "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                                })
                    ConversationInstance.update(conversation)
        return {"passed": True, "data": result}
    except Exception as e:
        print("===========conversationRefresh==========", e)
        return {
            "passed": False,
            "message": "Failed"
        }

