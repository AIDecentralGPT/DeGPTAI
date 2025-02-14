from tavily import TavilyClient
from pydantic import BaseModel
import re
import requests

api_key = "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"
tavily_client = TavilyClient(api_key=api_key)

class TavilySearchForm(BaseModel):
  keyword: str
  type: str

class tavilyClient:
  def search(self, keyword: str):
    try:
      response = tavily_client.search(
        query=keyword,
        include_images=True,
        include_image_descriptions=True,
        max_results=20
      )
      # 定义要屏蔽的 JavaScript 代码特征
      js_pattern = re.compile(r'var\s+hm\s*=\s*document\.createElement\("script"\);|function\s+bygjsw_switch_dark\(\)\{')
      # 过滤搜索结果
      web_result = []
      for result in response.get('results', []):
          content = result.get('content', '')
          if not js_pattern.search(content):
              web_result.append(result)
      image_result = []
      for result in response.get('images', []):
          image_result.append(result)
      return { "web": web_result, "images": image_result}
    except Exception as e:
      return None
  
TavilyClientApi = tavilyClient()