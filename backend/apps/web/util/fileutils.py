import requests
import mimetypes
import base64

class FileUtil:
  def url_to_data_url(self, file_url):
    """从URL下载文件并转换为Data URL"""
    response = requests.get(file_url)
    response.raise_for_status()
    
    # 从URL或响应头推断MIME类型
    mime_type = mimetypes.guess_type(file_url)[0] or response.headers.get("Content-Type") or "application/octet-stream"
    
    base64_data = base64.b64encode(response.content).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"
  
FileUtils = FileUtil()