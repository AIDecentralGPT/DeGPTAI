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
from apps.web.util.userutils import UserUtils
from apps.web.util.conversationutils import ConversationUtils



log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

# 更新用户聊天统计
@router.post("/refresh")
async def conversationRefresh(conversation_req: ConversationRequest, user=Depends(get_current_user)):
    try:
        # 获取当前请求模型信息
        modelinfo = ModelsInstance.get_info_by_model(conversation_req.model)

        # 获取用户VIP记录
        vipStatuss = VIPStatuses.get_vip_status_by_user_id(user.id)

        # 获取用户当前角色
        userrole = UserUtils.checkRole(user)

        # 获取当前日期
        date_time = date.today()

        # 获取非VIP用户目前角色当前会话数据
        conversation = ConversationInstance.get_info_by_user_mtype_date(user.id, userrole, modelinfo.type, date_time)

        # 获取用户当前可使用条数
        total = ConversationUtils.checkTotal(userrole, modelinfo.type, vipStatuss)

        print("==========可用会话总数==========:", total)

        # 获取用户的聊天次数
        user_total = ConversationUtils.checkUseTotal(user.id, userrole, conversation_req.equip_id, modelinfo.type, date_time, vipStatuss, conversation)
        print("==========已用会话总数==========:", user_total)

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
                if user_total < total:
                    #判断是否开启会员
                    if len(vipStatuss) > 0:
                        sorted_vipStatuss = sorted(vipStatuss, key=lambda x: (x.end_date, x.created_at))
                        for vipStatus in sorted_vipStatuss:
                            modellimit = ModelLimitInstance.get_info_by_user_vip("all", vipStatus.vip, modelinfo.type)
                            vipconversation = ConversationInstance.get_info_by_user_mtype_vip_date(user.id, userrole, modelinfo.type, vipStatus.vip, date_time)
                            if vipconversation is None:
                                ConversationInstance.insert(user.id, userrole, conversation_req.equip_id, modelinfo.type, vipStatus.vip, 1)
                                break
                            else:
                                if (vipconversation.chat_num < modellimit.limits):
                                    vipconversation.chat_num += 1
                                    ConversationInstance.update(vipconversation)
                                    break

                        result.append({
                            "passed": True,
                            "model": conversation_req.model,
                            "num": 1,
                            "message": "Success"
                        })
                            
                    else:
                        chat_num = user_total + 1
                        if conversation is None:
                            ConversationInstance.insert(user.id, userrole, conversation_req.equip_id, modelinfo.type, None, chat_num)
                        else:
                            conversation.chat_num = chat_num
                            ConversationInstance.update(conversation)
                        result.append({
                            "passed": True,
                            "model": conversation_req.model,
                            "num": 1,
                            "message": "Success"
                        })
                else:
                    if userrole == "wallet" and len(vipStatuss) == 0:
                        if conversation is None:
                            ConversationInstance.insert(user.id, userrole, conversation_req.equip_id, modelinfo.type, None, user_total)
                        else:
                            conversation.chat_num = user_total
                            ConversationInstance.update(conversation)
                    result.append({
                        "passed": False,
                        "model": conversation_req.model,
                        "num": 0,
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
        

