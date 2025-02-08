from fastapi import APIRouter, Depends, HTTPException, Request
from utils.utils import get_verified_user
from apps.web.models.kyc_restrict import KycRestrictInstance, CheckKycRequest, BindEmailRequest, BindCaptchaRequest, BindTrackingRequest
from datetime import datetime, timedelta


router = APIRouter()

# 添加IP记录
@router.post("/check_kyc")
async def check_kyc(request: Request, user=Depends(get_verified_user)):
    try:
        # 获取客户端IP
        client_ip = request.client.host
        # 校验用户是否再kyc认证中
        kycrestrict = KycRestrictInstance.get_by_userid(user.id)
        if kycrestrict is not None:
            if kycrestrict.status:
                return user
            else:
                time_difference = datetime.now() - kycrestrict.created_date
                if time_difference > timedelta(minutes=10):
                    kycrestrict = KycRestrictInstance.update_date(user.id, client_ip)
                    return {"pass": True, "data": user}
                else:
                    return {"pass": False, "message": "KYC verification is limited to once every 10 minutes, Please try again later."}
        
        # 判断同一个IP是否正在进中kyc的有两个
        kycrestricts = KycRestrictInstance.get_by_ip(client_ip)
        if  kycrestricts is not None and len(kycrestricts) >= 2:
            for kycrestrict in kycrestricts:
                # 计算时间差
                time_difference = datetime.now() - kycrestrict.created_date
                if time_difference > timedelta(minutes=10):
                    # 移除超过10分钟数据
                    kycrestricts.remove(kycrestrict)
                    # 如果超过10分钟未认证成功则删除数据
                    if kycrestrict.status == False:
                        KycRestrictInstance.remove(kycrestrict.user_id)
        if  kycrestricts is not None and len(kycrestricts) >= 2:
            return {"pass": False, "message": "A single IP address can be used for a maximum of two KYC verifications"}
        kycrestrict = KycRestrictInstance.insert(user.id, client_ip, None, None)
        if  kycrestrict is None:
            return {"pass": False, "message": "Check kyc failed, Please try again."}
        else:
            return {"pass": True, "data": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# 绑定邮箱
@router.post("/bind_email")
async def bind_email(bindemail: BindEmailRequest, user=Depends(get_verified_user)):
    try:
        kycrestrict = KycRestrictInstance.update_email(user.id, bindemail.email)
        if kycrestrict is None:
            raise HTTPException(status_code=400, detail="The binding of email failed")
        else:
            return kycrestrict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# 绑定图片认证
@router.post("/bind_captcha")
async def bind_captcha(bindcaptcha: BindCaptchaRequest, user=Depends(get_verified_user)):
    try:
        kycrestrict = KycRestrictInstance.update_capcher(user.id, bindcaptcha.captcha_code)
        if kycrestrict is None:
            raise HTTPException(status_code=400, detail="The binding of the picture authentication failed")
        else:
            return kycrestrict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# 绑定埋点
@router.post("/bind_tracking")
async def bind_tracking(bindtracking: BindTrackingRequest, user=Depends(get_verified_user)):
    try:
        kycrestrict = KycRestrictInstance.update_tracking(user.id, bindtracking.tracking)
        if kycrestrict is None:
            raise HTTPException(status_code=400, detail="The binding of tracking failed")
        else:
            return kycrestrict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))