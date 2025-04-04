from playwright.async_api import async_playwright
from pydantic import BaseModel


class WebInfoForm(BaseModel):
  url: str

class WebApi:
    async def getWebGraph(self, website: str):
        try:
            webInfo = {"title":"", "content": ""}
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(website)
                title = await page.title()
                webInfo["title"] = title
                # 提取页面的纯文本内容
                text_content = await page.inner_text('body')
                webInfo["content"] = text_content
                await browser.close()
            return webInfo
        except Exception as e:
            print("=================", e)
            return None
  
WebApiInstance = WebApi()