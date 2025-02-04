from fastapi import APIRouter
from fastapi import Depends, HTTPException
from utils.utils import get_verified_user
from apps.web.api.tavily import TavilyClientApi, TavilySearchForm
from apps.web.api.youtube import YoutubeClientApi, YoutubeSearchForm
from apps.web.api.twitter import TwitterApi, TwitterSearchForm


router = APIRouter()

@router.post("/tavily/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm):
    data = TavilyClientApi.search(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": data }

@router.post("/youtube/search", response_model=dict)
async def youtubeSearch(form: YoutubeSearchForm):
    print("==============================", form.keyword)
    response = YoutubeClientApi.search(form.keyword)
    if response is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return response
    
@router.post("/youtube/html/search", response_model=dict)
async def youtubeHtmlSearch(form: YoutubeSearchForm):
    print("==============================", form.keyword)
    html = YoutubeClientApi.fetch_youtube_page(form.keyword)
    if html:
        videos = YoutubeClientApi.parse_youtube_page(html)
        for video in videos:
            print(f"Title: {video['title']}, Link: {video['link']}")
        return { "ok": True, "data": videos }
    else:
        raise HTTPException(status_code=500, detail="未获取到信息")
    
@router.post("/twitter/search", response_model=dict)
async def twitterSearch(form: TwitterSearchForm):
    data = TwitterApi.search(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": data }
    
@router.post("/twitter/html/search", response_model=dict)
async def twitterSearch(form: TwitterSearchForm):
    data = TwitterApi.searchHtml(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": data }