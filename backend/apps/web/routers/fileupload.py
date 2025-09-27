from fastapi import APIRouter
from apps.web.util.aliossutils import AliOSSUtil
from apps.web.models.fileupload import UploadBase

router = APIRouter()

@router.post("/base")
async def upload_base64(upload: UploadBase):
  file_url = AliOSSUtil.upload_base64_to_oss(upload.data)
  return file_url