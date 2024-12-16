from fastapi import APIRouter, Depends, HTTPException
from apps.web.models.errorlog import ErrorLogInstance, ErrorLogRequest

router = APIRouter()

# 添加IP记录
@router.post("/add")
async def add_err_log(errlog: ErrorLogRequest):
    try:
        errorlog = ErrorLogInstance.insert_errorlog(errlog.err)
        return errorlog
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
