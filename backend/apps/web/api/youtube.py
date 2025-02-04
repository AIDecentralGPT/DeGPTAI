from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

class YoutubeSearchForm(BaseModel):
  keyword: str

api_key = "AIzaSyDwSyljiZVnzknJF-vjhPKh8R52nQGU_qI"

class YoutubeClient:
  def search(self, keyword: str):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        print("=========================", youtube)
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
    except Exception as e:
        print(f"发生错误: {e}")
        return None

  def fetch_youtube_page(self, query: str):
    url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch the page")
        return None
    
  def parse_youtube_page(self, html: str):
    soup = BeautifulSoup(html, 'html.parser')
    print("=========================", soup)
    videos = []
    for video in soup.find_all('a', {'class': 'yt-uix-tile-link'}):
        title = video.get('title')
        link = video.get('href')
        if title and link:
            videos.append({'title': title, 'link': 'https://www.youtube.com' + link})
    return videos

  
YoutubeClientApi = YoutubeClient()