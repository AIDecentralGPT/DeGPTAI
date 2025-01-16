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
        # 获取今天的聊天次数
        date_time = date.today()
        conversation = ConversationInstance.get_info_by_userid_model_date(user.id, conversation_req.model, date_time)

        # 获取用户是否为vip用户
        vipflag = VIPStatuses.is_vip_active(user.id)

        # 获取模型的聊天次数
        modellimit = ModelLimitInstance.get_info_by_model(conversation_req.model)
        if modellimit is None:
            return {
                "passed": True,
                "message": "There is no such model"
            }

        # 判断用户是否超出次数
        if conversation is not None:
            print("============================", modellimit.normal != -1, modellimit.normal <= conversation.chat_num)
            if vipflag:
                print("====================vip=====================")
                if modellimit.vip != -1 and modellimit.vip <= conversation.chat_num:
                    return {
                        "passed": False,
                        "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                    }
            else:
                print("====================normal=====================")
                if modellimit.normal != -1 and modellimit.normal <= conversation.chat_num:
                    print("=========================================")
                    return {
                        "passed": False,
                        "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                    }

        if conversation is None:
            ConversationInstance.insert(user.id, conversation_req.model)
        else:
            ConversationInstance.update(conversation)
        return {
            "passed": True,
            "message": "Success"
        }
    except Exception as e:
        print("==========================", e)
        return {
            "passed": True,
            "message": "Failed"
        }

