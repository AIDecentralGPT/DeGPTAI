import tweepy
from twscrape import API
from pydantic import BaseModel
import requests
import os
from bs4 import BeautifulSoup

from playwright.sync_api import sync_playwright
import time

consumer_key = os.getenv("dev_consumer_key")
consumer_secret = os.getenv("dev_consumer_secret")
bearer_token = os.getenv("dev_bearer_token")
access_token = os.getenv("dev_access_token")
access_token_secret = os.getenv("dev_access_token_secret")

SOCIAL_KEY = os.getenv("SOCIAL_KEY")

class TwitterSearchForm(BaseModel):
  keyword: str

class TwitterLib:
    def __init__(self):
        # 进行身份验证
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        # 创建API对象，用于后续操作
        self.api = tweepy.API(auth)
        # 创建客户端对象
        self.client = tweepy.Client(bearer_token)

    def check_follow_status(self, follower_username: str, target_username: str):
        try:
            # 获取关注者的用户对象
            follower_user = self.api.get_user(screen_name=follower_username)
            print("=========follower_user=========", follower_user)
            # 获取目标账号的用户对象
            target_user = self.api.get_user(screen_name=target_username)
            # 检查关注关系，使用show_friendship方法，它返回一个包含两个用户关系信息的元组
            relationship = self.api.show_friendship(
                source_id=follower_user.id, target_id=target_user.id)
            # 元组中的第二个元素（索引为1）对应着关注者是否关注目标账号的布尔值
            return relationship[1]
        except tweepy.TweepyException as e:
            print(f"出现错误：{e}")
            return False
        
    def search(self, keword: str):
        try:
            # 搜索包含特定关键词的推文
            tweets = self.api.search_tweets(q=keword, count=10)
            for tweet in tweets:
                print("==========tweet===========", tweet)   
            return tweets
        except Exception as e:
            print(f"出现错误：{e}")
            return None
        
    def search_social(self, keword: str):
        url = f'https://api.socialdata.tools/twitter/search?query={keword}&type=Latest'
        headers = {
            'Authorization': f'Bearer {SOCIAL_KEY}',
            'Accept': 'application/json'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                if data.get("tweets"):
                    # 使用字典推导式过滤重复的 id
                    unique_dict = {item["user"]["id"]: item for item in data.get("tweets")}
                    unique_data = list(unique_dict.values())
                    return {"content": unique_data}
                else:
                    return None
            else:
                return None
        except requests.exceptions.HTTPError as err:
            print("具体401错误信息:", response.text)
            return None
        except requests.exceptions.RequestException as err:
            print(f"请求异常: {err}")
            return None

    async def search_twscrape(self, keword: str):
        api = API()
        accounts = await api.pool.get_all()
        if not any(acc.username == "BrookeHamp25599" for acc in accounts):
            print("==========添加账号===========")
            await api.pool.add_account("BrookeHamp25599", "i1FpNoLs6EIVsUiu", "ydarsmjzaq@rambler.ru")
        
        await api.pool.login_all()     
        tweets = []
        async for tweet in api.search(keword, limit=10):
            tweets.append({
                "text": tweet.rawContent,
                "username": tweet.user.username,
                "date": tweet.date,
                "url": f"https://x.com/{tweet.user.username}/status/{tweet.id}",
            })
        return tweets

    def scrape_nitter(self, keyword):
        url = f"https://nitter.net/search?f=tweets&q={keyword}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        print("=====================", r)
        soup = BeautifulSoup(r.text, "html.parser")
        
        tweets = soup.select('.timeline-item .tweet-content')
        for tweet in tweets[:5]:
            print("=============", tweet.text.strip())
        
        return []
    
    async def scrape_twitter(self, keyword):
        async with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = f"https://twitter.com/search?q={keyword}&src=typed_query&f=live"
            page.goto(url)
            time.sleep(5)  # 等待加载

            tweets = page.query_selector_all('article div[lang]')
            for tweet in tweets[:5]:  # 抓前5条
                print(tweet.inner_text())

            browser.close()

TwitterApi = TwitterLib()
