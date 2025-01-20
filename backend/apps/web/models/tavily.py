from tavily import TavilyClient
from pydantic import BaseModel

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key="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")

class TavilySearchForm(BaseModel):
  keywords: str

class tavilyClient:
  def search(self, keyword: str):
    try:
      response = tavily_client.search(keyword)
      return response
    except Exception as e:
      print("=======================", e)
      return None
  
TavilyClientInstance = tavilyClient()