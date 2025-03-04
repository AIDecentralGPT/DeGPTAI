import requests
from pydantic import BaseModel

class YoutubeSearchForm(BaseModel):
  keyword: str

API_KEY = "******************************"

class YoutubeClient:
  def search(self, keyword: str):
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        # Call the search(). list() method to perform a search
        params = {
            "key": API_KEY,
            "q": keyword,
            "part": "snippet",
            "type": "video",
            "maxResults": 10,
            "order": "relevance"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        # Print search results
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
        print(f"An error occurred: {e}")
        return None

YoutubeClientApi = YoutubeClient()