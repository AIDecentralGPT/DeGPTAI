from fastapi import APIRouter
from fastapi import Depends, HTTPException
from utils.utils import get_verified_user
from apps.web.api.tavily import TavilyClientApi, TavilySearchForm
from apps.web.api.youtube import YoutubeClientApi, YoutubeSearchForm
from apps.web.api.twitter import TwitterApi, TwitterSearchForm
from concurrent.futures import ThreadPoolExecutor


router = APIRouter()


@router.post("/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm):
    if form.type == 'twitter':
        data = TwitterApi.search_social(form.keyword)
        return { "ok": True, "data": data}
    elif form.type == 'youtube':
        data = YoutubeClientApi.search(form.keyword)
        return { "ok": True, "data": data}
    else:
        data = TavilyClientApi.search(form.keyword)
        return { "ok": True, "data": data}


@router.post("/tavily/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm):
    data = TavilyClientApi.search(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": data }
    
@router.post("/twitter/search", response_model=dict)
async def twitterSearch(form: TwitterSearchForm):
    data = TwitterApi.search(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": data }
    
@router.post("/social/search", response_model=dict)
async def twitterSearch(form: TwitterSearchForm):
    data = TwitterApi.search_social(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": data }

@router.post("/youtube/search", response_model=dict)
async def youtubeSearch(form: YoutubeSearchForm):
    videos = YoutubeClientApi.search(form.keyword)
    if videos is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": videos }