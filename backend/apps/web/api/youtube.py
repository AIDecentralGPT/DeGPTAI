from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel

class YoutubeSearchForm(BaseModel):
  keyword: str

api_key = "AIzaSyDwSyljiZVnzknJF-vjhPKh8R52nQGU_qI"

class YoutubeClient:
  def search(self, keyword: str):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        # 调用 search().list() 方法进行搜索
        request = youtube.search().list(
            part="snippet",
            q=keyword,
            type="video",
            maxResults=10  # 最多返回 10 条结果
        )
        response = request.execute()
        # 打印搜索结果
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            print(f"Video ID: {video_id}, Title: {video_title}")
        return response.get("items", [])
    except HttpError as e:
        print(f"发生错误: {e}")
        return None
  
YoutubeClientInstance = YoutubeClient()