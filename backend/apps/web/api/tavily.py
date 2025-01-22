from tavily import TavilyClient
from pydantic import BaseModel

tavily_client = TavilyClient(api_key="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")

class TavilySearchForm(BaseModel):
  keyword: str

class tavilyClient:
  def search(self, keyword: str):
    try:
      response = tavily_client.search(keyword)
      return response
    except Exception as e:
      print("=======================", e)
      return None
  
TavilyClientInstance = tavilyClient()