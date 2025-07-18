from apps.web.models.model_limit import ModelLimitInstance
from apps.web.models.conversation import ConversationInstance
from apps.web.models.vipstatus import VIPStatusModelResp
from apps.web.models.conversation import ConversationModel
from datetime import date
from typing import List

class ConversationUtil:

  # 获取用户可使用总条数
  def checkTotal(self, user_role: str, model_type: str, vipStatuss: List[VIPStatusModelResp]):
    # 获取用户当前可使用条数
    total = 0
    if len(vipStatuss) > 0:
      for vipStatus in vipStatuss:
        viplimit = ModelLimitInstance.get_info_by_user_vip("all", vipStatus.vip, model_type)
        if viplimit:
          total += viplimit.limits
    # 非VIP用户获取免费条数
    else:
      freelimit = ModelLimitInstance.get_info_by_user_vip(user_role, "free", model_type)
      if freelimit:
        total += freelimit.limits
    return total
  
  # 获取用户已用会话数
  def checkUseTotal(self, user_id: str, user_role: str, equip_id: str, model_type: str, date_time: date, vipStatuss: List[VIPStatusModelResp], conversation: ConversationModel):
    if len(vipStatuss) > 0:
      min_vipstatus = min(vipStatuss, key=lambda x: x.start_date)
      month_total = ConversationInstance.get_info_by_userid_mtype_between(user_id, model_type, min_vipstatus.start_date)
      return month_total
    else:
      if user_role == "wallet":
        converation_max = ConversationInstance.get_info_by_equipid(equip_id, user_role, model_type, date_time)
        if converation_max is not None:
          return converation_max.chat_num
        else:
          return 0 if conversation is None else conversation.chat_num
      else:
        return 0 if conversation is None else conversation.chat_num
    
  
# 实例化ConversationUtil类
ConversationUtils = ConversationUtil()