from playwright.async_api import async_playwright
from pydantic import BaseModel
import requests


class WebInfoForm(BaseModel):
  url: str

class WebApi:
    async def getWebGraph(self, website: str):
        webInfo = {"title":"", "content": ""}
        if not(website.startswith('https://') or website.startswith('http://')):
            websitetran = f"https://{website}"
            response = requests.get(website, timeout=5)
            if response.status_code != 200:
                websitetran = f"http://{website}"
        try: 
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(websitetran)
                title = await page.title()
                webInfo["title"] = title
                # 提取页面的纯文本内容
                text_content = await page.inner_text('body')
                webInfo["content"] = text_content
                await browser.close()
            return webInfo
        except Exception as e:
            print("=================", e)
            return webInfo
  
WebApiInstance = WebApi()