from fastapi import File, UploadFile
from datetime import datetime
from config import DATA_DIR
import requests
import mimetypes
import base64
import uuid
import os

# 定义文件上传文件夹并创建
UPLOAD_DIR = f"{DATA_DIR}/uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class FileUtil:
    def url_to_data_url(self, file_url):
        """从URL下载文件并转换为Data URL"""
        response = requests.get(file_url)
        response.raise_for_status()

        # 从URL或响应头推断MIME类型
        mime_type = (
            mimetypes.guess_type(file_url)[0]
            or response.headers.get("Content-Type")
            or "application/octet-stream"
        )

        base64_data = base64.b64encode(response.content).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"

    # 校验文件后缀名
    def check_ext(self, filename: str):
        file_ext = filename.split(".")[-1].lower()
        known_type = False
        anaylis_type = "file"
        known_file_ext = [
            "pdf",
            "ppt",
            "pptx",
            "doc",
            "docx",
            "rtf",
            "xls",
            "xlsx",
            "csv",
            "txt",
            "log",
            "xml",
            "ini",
            "json",
            "md",
            "zip",
            "rar",
        ]

        if file_ext in known_file_ext:
            anaylis_type = "file"
            known_type = True
        elif file_ext in self.contain_ext():
            anaylis_type = "progrem"
            known_type = True

        return file_ext, known_type, anaylis_type
    
    # 将文件内容保存到本地
    def save_file(self, file_ext: str, file: UploadFile = File(...)):
        # 获取当前日期时间
        current_date = datetime.now()
        # 格式化为年月日字符串（示例输出：2023-10-05）
        date_str = current_date.strftime("%Y-%m-%d")
        file_dir = f"{UPLOAD_DIR}/{date_str}"
        # 创建文件夹
        os.makedirs(file_dir, exist_ok=True)
        
        file_path = f"{file_dir}/{str(uuid.uuid4())}.{file_ext}"
        contents = file.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
            f.close()
        return file_path
    
    # 删除文件
    def remove_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)


FileUtils = FileUtil()
