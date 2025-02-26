from tavily import TavilyClient
from pydantic import BaseModel
import re
import requests
import jieba

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
        include_answer="basic",
        include_images=True,
        include_image_descriptions=True,
        max_results=8
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
      words = jieba.cut(keyword, cut_all=True)
      return {"keyword": "/".join(words), "web": web_result, "images": image_result}
    except Exception as e:
      print("==========================", e)
      return None
  
TavilyClientApi = tavilyClient()