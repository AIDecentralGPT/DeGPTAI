import tweepy
from pydantic import BaseModel
import re
import requests
from bs4 import BeautifulSoup


consumer_key = 'q9r7Zv527UosaDGPcYDJZ8wih'
consumer_secret = 'dbIBdjsKpqffGMNZ8bHqLg9N8uTnBz0py4aCy9397C2vJknFgz'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAADX0vAEAAAAA%2FGkhIQJvPdj0YR%2FsQT8dJak0OgI%3Dh0TUAu5TFYUFKO5pRnSfhg1k8KXBO4KTGKmszkqwGrK6hUwbl5'
access_token = '1726080863979610112-xWTMVvhOHAPJa0C81lwVNYWzQEUL6F'
access_token_secret = 'glwphg8uY4Mlr7etrYxu8PB6PbVFzH0tTp7tmx8Jd8Ly8'


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
            tweets = self.client.search_recent_tweets(query=keword, max_results=10, 
                expansions='attachments.media_keys', media_fields=['preview_image_url', 'url'])
            # 存储媒体对象，键为media_key，值为媒体对象
            media = {m["media_key"]: m for m in tweets.includes.get('media', [])}
            # 定义匹配 URL 的正则表达式模式
            url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            # 用于存储最终结果的列表
            tweet_list = []
            if tweets.data:
                for tweet in tweets.data:
                    tweet_text = tweet.text
                    # 查找所有链接
                    urls = url_pattern.findall(tweet_text)
                    # 移除链接后的文本内容
                    text_without_urls = url_pattern.sub('', tweet_text).strip()
                    tweet_info = {
                        "text": text_without_urls,
                        "urls": urls,
                        "media_urls": []
                    }
                    attachments = tweet.data.get('attachments')
                    if attachments and 'media_keys' in attachments:
                        for media_key in attachments['media_keys']:
                            if media_key in media:
                                # 获取媒体对象
                                media_info = media[media_key]
                                if 'preview_image_url' in media_info:
                                    tweet_info["media_urls"].append(media_info['preview_image_url'])
                                elif 'url' in media_info:
                                    tweet_info["media_urls"].append(media_info['url'])
                    tweet_list.append(tweet_info)
                return tweet_list
            else:
                return None
        except Exception as e:
            print(f"出现错误：{e}")
            return None
        
    def searchHtml(self, keyword: str):
        # 要请求的网址
        url = f'https://x.com/search?q={keyword}&src=typed_query'
        try:
            # 发送 GET 请求
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            tweets = soup.find_all("div", class_="tweet")
            print(tweets)
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP 错误发生: {http_err}')
        except requests.exceptions.RequestException as req_err:
            print(f'请求发生错误: {req_err}')
        return None

TwitterApi = TwitterLib()
