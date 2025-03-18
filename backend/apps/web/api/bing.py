import requests
import os
import json
import jieba
import re

# API 密钥
subscription_key = os.getenv("BING_KEY")
search_url = os.getenv("BING_URL")

bocai_key = os.getenv("BOCHAAI_KEY")
bocai_url = os.getenv("BOCHAAI_URL")

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
            return search_results
        except Exception as err:
            print(f"其他错误发生: {err}")
            return None
        
    def bcsearch(self, keyword: str):     
        try:
            headers = {
                'Authorization': f'Bearer {bocai_key}',
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "query": keyword,
                "summary": True,
                "count": 15,
                "page": 1
            })
            response = requests.request("POST", bocai_url, headers=headers, data=payload)
            response_json = response.json()
            web_result = []
            image_result = []
            if response_json.get("code") == 200:
                search_results = response_json.get("data")
                for result in search_results.get("webPages", {}).get("value", []):
                    webdata = {"title": result.get("name"),
                            "content": result.get("summary"),
                            "url": result.get("url")}
                    web_result.append(webdata)
                for result in search_results.get("images", {}).get("value", []):
                    imgdata = {"url": result.get("contentUrl"),
                            "description": result.get("contentUrl")}
                    image_result.append(imgdata)
                pattern = r'[^\w\s]'
                keyword = re.sub(pattern, '', keyword)
                words = jieba.cut(keyword, cut_all=False)
                return {"keyword": "/".join(words), "web": web_result, "images": image_result}
            else:
                return None
        except Exception as err:
            print(f"其他错误发生: {err}")
            return None

BingApiInstance = BingApi()