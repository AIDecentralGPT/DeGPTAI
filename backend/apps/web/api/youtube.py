import requests
from pydantic import BaseModel
<<<<<<< HEAD
=======
import os
>>>>>>> fingerprintAuth-out

class YoutubeSearchForm(BaseModel):
  keyword: str

<<<<<<< HEAD
API_KEY = "******************************"
=======
API_KEY = os.getenv("Youtube_Key")
>>>>>>> fingerprintAuth-out

class YoutubeClient:
  def search(self, keyword: str):
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
<<<<<<< HEAD
        # Call the search(). list() method to perform a search
=======
        # 调用 search().list() 方法进行搜索
>>>>>>> fingerprintAuth-out
        params = {
            "key": API_KEY,
            "q": keyword,
            "part": "snippet",
            "type": "video",
            "maxResults": 10,
            "order": "relevance"
        }
        response = requests.get(url, params=params)
<<<<<<< HEAD
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        # Print search results
=======
        response.raise_for_status()  # 检查HTTP错误
        data = response.json()
        # 打印搜索结果
>>>>>>> fingerprintAuth-out
        videos = []
        for item in data.get("items", []):
            if "id" in item and "videoId" in item["id"]:
                video_id = item["id"]["videoId"]
                snippet = item["snippet"] 
                video_info = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "description": snippet["description"],
                    "published_at": snippet["publishedAt"],
                    "channel_title": snippet["channelTitle"],
                    "thumbnail_url": snippet["thumbnails"]["high"]["url"],
                    "video_url": f"https://www.youtube.com/watch?v={video_id}"
                }
                videos.append(video_info)
        return {"videos": videos}
    except Exception as e:
<<<<<<< HEAD
        print(f"An error occurred: {e}")
=======
        print(f"发生错误: {e}")
>>>>>>> fingerprintAuth-out
        return None

YoutubeClientApi = YoutubeClient()