from fastapi import APIRouter
from fastapi import Depends, HTTPException
from utils.utils import get_verified_user
from apps.web.api.tavily import TavilyClientApi, TavilySearchForm
from apps.web.api.youtube import YoutubeClientApi, YoutubeSearchForm
from apps.web.api.twitter import TwitterApi, TwitterSearchForm
import random


router = APIRouter()

@router.post("/tavily/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm):
    data = TavilyClientApi.search(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": data }
    

@router.post("/video/search", response_model=dict)
async def videoSearch(form: YoutubeSearchForm):
    data = []
    twitterData = TwitterApi.search(form.keyword)
    if twitterData is not None:
        data.extend(twitterData)
    youtubeData = YoutubeClientApi.search(form.keyword)
    if youtubeData is not None:
        data.extend(youtubeData)
    # 打乱列表顺序
    random.shuffle(data)
    return { "ok": True, "data": data }

    
@router.post("/twitter/search", response_model=dict)
async def twitterSearch(form: TwitterSearchForm):
    data = TwitterApi.search(form.keyword)
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