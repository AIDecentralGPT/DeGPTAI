from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from apps.web.util.aliossutils import AliOSSUtil
from apps.web.models.fileupload import UploadBase
from typing import Optional
import os
from pathlib import Path

from apps.web.util.fileutils import FileUtils
from apps.web.util.aliossutils import AliOSSUtil
from apps.web.util.pdfconverter import FileToPDFConverter

router = APIRouter()

@router.post("/base")
async def upload_base64(upload: UploadBase):
  file_url = AliOSSUtil.upload_base64_to_oss(upload.data)
  return file_url

@router.post("/file")
def store_doc(
    collection_name: Optional[str] = Form(None),
    file: UploadFile = File(...),
):
    result = {
        "collection_name": "",
        "known_type": False,
        "anaylis_type": "file",
        "url": ""
    }
    try:
        unsanitized_filename = file.filename
        filename = os.path.basename(unsanitized_filename)
        result["collection_name"] = filename

        # 校验文件是否支持分析
        file_ext, known_type, anaylis_type = FileUtils.check_ext(filename)
        result["known_type"] = known_type
        result["anaylis_type"] = anaylis_type

        # Upload file
        file_path = FileUtils.save_file(file_ext, file)
        # convert file
        conver_path = FileToPDFConverter.convert(file_path)
        path = Path(conver_path)
        file_ext = path.suffix[1:]

        # 根据文件上传阿里OSS
        oss_path = AliOSSUtil.upload_file_to_oss(conver_path, file_ext)
        result["url"] = oss_path

        # 删除本地文件
        FileUtils.remove_file(file_path)
        if file_path != conver_path:
          FileUtils.remove_file(conver_path)
        return result
    except Exception as e:
        FileUtils.remove_file(file_path)
        if file_path != conver_path:
          FileUtils.remove_file(conver_path)
        raise HTTPException(status_code=400, detail=e.detail)