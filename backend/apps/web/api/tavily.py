from tavily import TavilyClient
from pydantic import BaseModel
import re

tavily_client = TavilyClient(api_key="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")

class TavilySearchForm(BaseModel):
  keyword: str

class tavilyClient:
  def search(self, keyword: str):
    try:
      response = tavily_client.search(keyword)
      # 定义要屏蔽的 JavaScript 代码特征
      js_pattern = re.compile(r'var\s+hm\s*=\s*document\.createElement\("script"\);|function\s+bygjsw_switch_dark\(\)\{')
      # 过滤搜索结果
      filtered_results = []
      for result in response.get('results', []):
          content = result.get('content', '')
          if not js_pattern.search(content):
              filtered_results.append(result)
      return filtered_results
    except Exception as e:
      print("=======================", e)
      return None
  
TavilyClientApi = tavilyClient()