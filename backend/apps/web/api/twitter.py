import tweepy
from pydantic import BaseModel
import requests
<<<<<<< HEAD


consumer_key = '***********'
consumer_secret = '**********************'
bearer_token = '*********************************'
access_token = '*************************'
access_token_secret = '***************************'

social_key = "*************************************"
=======
import os


consumer_key = os.getenv("dev_consumer_key")
consumer_secret = os.getenv("dev_consumer_secret")
bearer_token = os.getenv("dev_bearer_token")
access_token = os.getenv("dev_access_token")
access_token_secret = os.getenv("dev_access_token_secret")

SOCIAL_KEY = os.getenv("SOCIAL_KEY")
>>>>>>> fingerprintAuth-out


class TwitterSearchForm(BaseModel):
  keyword: str

class TwitterLib:
    def __init__(self):
<<<<<<< HEAD
        # Perform identity verification
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        # Create API objects for subsequent operations
        self.api = tweepy.API(auth)
        # Create client object
=======
        # 进行身份验证
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        # 创建API对象，用于后续操作
        self.api = tweepy.API(auth)
        # 创建客户端对象
>>>>>>> fingerprintAuth-out
        self.client = tweepy.Client(bearer_token)

    def check_follow_status(self, follower_username: str, target_username: str):
        try:
<<<<<<< HEAD
            # Obtain user objects of followers
            follower_user = self.api.get_user(screen_name=follower_username)
            print("=========follower_user=========", follower_user)
            # Obtain the user object of the target account
            target_user = self.api.get_user(screen_name=target_username)
            # Check the attention relationship using the show_friendship method, which returns a tuple containing information about two user relationships
            relationship = self.api.show_friendship(
                source_id=follower_user.id, target_id=target_user.id)
            # The second element in the tuple (indexed as 1) corresponds to the Boolean value of whether the follower follows the target account or not
            return relationship[1]
        except tweepy.TweepyException as e:
            print(f"An error occurred: {e}")
=======
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
>>>>>>> fingerprintAuth-out
            return False
        
    def search(self, keword: str):
        try:
<<<<<<< HEAD
            # Search for tweets containing specific keywords
            headers = {"Authorization": f"Bearer {bearer_token}"}
            # Search for recent tweets containing 'Python' (within the past 7 days)
            url = "https://api.twitter.com/2/tweets/search/recent"
            params = {
                "query": keword,          # Search keywords
                "max_results": 10,          # Return quantity
=======
            # 搜索包含特定关键词的推文
            headers = {"Authorization": f"Bearer {bearer_token}"}
            # 搜索最近包含 "Python" 的推文（过去 7 天内）
            url = "https://api.twitter.com/2/tweets/search/recent"
            params = {
                "query": keword,          # 搜索关键字
                "max_results": 10,          # 返回数量
>>>>>>> fingerprintAuth-out
                "tweet.fields": "created_at,public_metrics"
            }
            response = requests.get(url, headers=headers, params=params)
            tweets = response.json()
            if tweets.get("data"):
                return {"content": tweets.get("data")}
            else:
                return None
        except Exception as e:
<<<<<<< HEAD
            print(f"An error occurred：{e}")
=======
            print(f"出现错误：{e}")
>>>>>>> fingerprintAuth-out
            return None
        
    def search_social(self, keword: str):
        url = f'https://api.socialdata.tools/twitter/search?query={keword}&type=Latest'
        headers = {
<<<<<<< HEAD
            'Authorization': f'Bearer {social_key}',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("tweets"):
                # Using dictionary deduction to filter duplicate entries id
                unique_dict = {item["user"]["id"]: item for item in data.get("tweets")}
                unique_data = list(unique_dict.values())
                return {"content": unique_data}
            else:
                return None
            return data
        else:
=======
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
>>>>>>> fingerprintAuth-out
            return None

TwitterApi = TwitterLib()
