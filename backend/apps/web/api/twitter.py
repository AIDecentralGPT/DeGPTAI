import tweepy
from pydantic import BaseModel
import requests


consumer_key = '***********'
consumer_secret = '**********************'
bearer_token = '*********************************'
access_token = '*************************'
access_token_secret = '***************************'

social_key = "*************************************"


class TwitterSearchForm(BaseModel):
  keyword: str

class TwitterLib:
    def __init__(self):
        # Perform identity verification
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        # Create API objects for subsequent operations
        self.api = tweepy.API(auth)
        # Create client object
        self.client = tweepy.Client(bearer_token)

    def check_follow_status(self, follower_username: str, target_username: str):
        try:
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
            return False
        
    def search(self, keword: str):
        try:
            # Search for tweets containing specific keywords
            headers = {"Authorization": f"Bearer {bearer_token}"}
            # Search for recent tweets containing 'Python' (within the past 7 days)
            url = "https://api.twitter.com/2/tweets/search/recent"
            params = {
                "query": keword,          # Search keywords
                "max_results": 10,          # Return quantity
                "tweet.fields": "created_at,public_metrics"
            }
            response = requests.get(url, headers=headers, params=params)
            tweets = response.json()
            if tweets.get("data"):
                return {"content": tweets.get("data")}
            else:
                return None
        except Exception as e:
            print(f"An error occurred：{e}")
            return None
        
    def search_social(self, keword: str):
        url = f'https://api.socialdata.tools/twitter/search?query={keword}&type=Latest'
        headers = {
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
            return None

TwitterApi = TwitterLib()
