import tweepy

consumer_key = 'q9r7Zv527UosaDGPcYDJZ8wih'
consumer_secret = 'dbIBdjsKpqffGMNZ8bHqLg9N8uTnBz0py4aCy9397C2vJknFgz'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAADX0vAEAAAAA%2FGkhIQJvPdj0YR%2FsQT8dJak0OgI%3Dh0TUAu5TFYUFKO5pRnSfhg1k8KXBO4KTGKmszkqwGrK6hUwbl5'
access_token = '1726080863979610112-xWTMVvhOHAPJa0C81lwVNYWzQEUL6F'
access_token_secret = 'glwphg8uY4Mlr7etrYxu8PB6PbVFzH0tTp7tmx8Jd8Ly8'

class TwitterLib:
    def __init__(self):
        # 进行身份验证
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        # 创建API对象，用于后续操作
        self.api = tweepy.API(auth)

    def check_follow_status(self, follower_username, target_username):
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
        
twitter_lib = TwitterLib()
