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
        vipStatuss = VIPStatuses.get_vip_status_by_user_id(user.id)

        # 获取当前请求模型信息
        modelinfo = ModelsInstance.get_info_by_model(conversation_req.model)

        # 获取今天的聊天次数
        date_time = date.today()
        conversation = ConversationInstance.get_info_by_userid_mtype_date(user.id, modelinfo.type, date_time)
        month_total = ConversationInstance.get_info_by_userid_mtype_month(user.id, modelinfo.type, date_time)

        total = 0
        # 获取非VIP请求模型的总次数
        userrole = "user"
        if user.id.startswith("0x"):
            userrole = "wallet"
            if user.verified:
                userrole = "kyc"   
        freelimit = ModelLimitInstance.get_info_by_user_vip(userrole, "free", modelinfo.type)
        if freelimit:
            total = total + freelimit.limits

        # 获取VIP请求模型的总次数
        if len(vipStatuss) > 0:
            for vipStatus in vipStatuss:
                viplimit = ModelLimitInstance.get_info_by_user_vip("all", vipStatus.vip, modelinfo.type)
                if viplimit:
                    total = total + viplimit.limits

        print("==========会话总数==========:", total)

        # 校验用户是否超数量
        result = []
        if modelinfo is not None:
            # 总条数为0
            if total == 0:
                result.append({
                    "passed": False,
                    "model": conversation_req.model,
                    "num": 0,
                    "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                })
            else:
                if conversation is None:
                    # 基础模型直接添加数据
                    if modelinfo.type == "base":
                        ConversationInstance.insert(user.id, userrole, modelinfo.type)
                        result.append({
                            "passed": True,
                            "model": conversation_req.model,
                            "num": 0,
                            "message": "Success conversation base"
                        })
                    # 非基础模型判断是否是VIP
                    else:
                        if vipStatus is not None:
                            ConversationInstance.insert(user.id, userrole, modelinfo.type)
                            result.append({
                                "passed": True,
                                "model": conversation_req.model,
                                "num": 0,
                                "message": "Success conversation vip"
                            })
                        else:
                            result.append({
                                "passed": False,
                                "model": conversation_req.model,
                                "num": conversation.chat_num,
                                "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                            })
                else:
                    if (conversation.chat_num + month_total) < total:
                        conversation.user_role = userrole
                        ConversationInstance.update(conversation)
                        result.append({
                            "passed": True,
                            "model": conversation_req.model,
                            "num": conversation.chat_num,
                            "message": "Success"
                        })
                    else:
                        result.append({
                            "passed": False,
                            "model": conversation_req.model,
                            "num": conversation.chat_num,
                            "message": "The number of attempts has exceeded the limit. Please upgrade to VIP."
                        })
                        
        else:
            result.append({
                "passed": True,
                "model": conversation_req.model,
                "num": 1,
                "message": "Success"
            })

        return {"passed": True, "data": result}
    except Exception as e:
        print("========================", e)
        return {
            "passed": False,
            "message": "Failed"
        }
    
@router.post("/total")
async def conversationTotal(user=Depends(get_current_user)):

    # 获取用户当前VIP信息
    vipStatuss = VIPStatuses.get_vip_status_by_user_id(user.id)

    # 获取今天的聊天次数
    date_time = date.today()

    result = ConversationInstance.get_info_by_userid_user_total(user, vipStatuss, date_time)

    return result
        

