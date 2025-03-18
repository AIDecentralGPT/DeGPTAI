import requests
import os

# API 密钥
subscription_key = os.getenv("BING_KEY")
search_url = os.getenv("BING_URL")

class BingApi:
  def search(self, keyword: str):     
    # 设置请求头
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {
        "q": keyword,
        "textDecorations": True,
        "textFormat": "HTML"
    }
    try:
      # 发送请求
      response = requests.get(search_url, headers=headers, params=params)
      response.raise_for_status()
      # 获取 JSON 格式的响应
      search_results = response.json()
      # 打印搜索结果
      for result in search_results.get("webPages", {}).get("value", []):
        print(f"标题: {result.get('name')}")
        print(f"链接: {result.get('url')}")
        print(f"摘要: {result.get('snippet')}")
        print("-" * 80)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
    except Exception as err:
        print(f"其他错误发生: {err}")

BingApiInstance = BingApi()