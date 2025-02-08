from fastapi import APIRouter, Depends, HTTPException, Request
from utils.utils import get_verified_user
from apps.web.models.kyc_restrict import KycRestrictInstance, CheckKycRequest, BindEmailRequest, BindCaptchaRequest, BindTrackingRequest
from datetime import datetime


router = APIRouter()

# 添加IP记录
@router.post("/check_kyc")
async def check_kyc(request: Request, user=Depends(get_verified_user)):
    try:
        # 校验用户是否再kyc认证中
        kycrestrict = KycRestrictInstance.get_by_userid(user.id)
        if kycrestrict is not None:
            if kycrestrict.status:
                return user
            else:
                time_difference = datetime.datetime.now() - kycrestrict.created_date
                if time_difference > 10:
                    kycrestrict = KycRestrictInstance.update_date(user.id)
                    return user
                else:
                    raise HTTPException(status_code=400, detail="The KYC verification is in progress")
        client_ip = request.client.host
        kycrestricts = KycRestrictInstance.get_by_ip(client_ip)
        if kycrestricts is not None and len(kycrestricts) > 2:
            raise HTTPException(status_code=400, detail="Ip limit failed")
            # for kycrestrict in kycrestricts:
            #     # 计算时间差
            #     time_difference = datetime.datetime.now() - kycrestrict.created_date
            #     if time_difference > 10:
            #         kycrestricts.remove(kycrestrict)
        kycrestrict = KycRestrictInstance.insert(user.id, client_ip, None, None)
        if kycrestrict is None:
            raise HTTPException(status_code=400, detail="Check kyc failed")
        else:
            return user
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