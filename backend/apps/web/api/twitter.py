import tweepy
from pydantic import BaseModel
import requests
import os


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
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
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
            headers = {"Authorization": f"Bearer {bearer_token}"}
            # 搜索最近包含 "Python" 的推文（过去 7 天内）
            url = "https://api.twitter.com/2/tweets/search/recent"
            params = {
                "query": keword,          # 搜索关键字
                "max_results": 10,          # 返回数量
                "tweet.fields": "created_at,public_metrics"
            }
            response = requests.get(url, headers=headers, params=params)
            tweets = response.json()
            if tweets.get("data"):
                return {"content": tweets.get("data")}
            else:
                return None
        except Exception as e:
            print(f"出现错误：{e}")
            return None
        
    def search_social(self, keword: str):
        url = f'https://api.socialdata.tools/twitter/search?query={keword}&type=Latest'
        headers = {
            'Authorization': f'Bearer {SOCIAL_KEY}',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
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

TwitterApi = TwitterLib()
