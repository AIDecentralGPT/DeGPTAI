from fastapi import APIRouter
from fastapi import Depends, HTTPException
from utils.utils import get_verified_user
from apps.web.api.tavily import TavilyClientApi, TavilySearchForm
from apps.web.api.youtube import YoutubeClientApi, YoutubeSearchForm
from apps.web.api.twitter import TwitterApi, TwitterSearchForm


router = APIRouter()

@router.post("/tavily/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm):
    print("==============================", form.keyword)
    response = TavilyClientApi.search(form.keyword)
    if response is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return response

@router.post("/youtube/search", response_model=dict)
async def youtubeSearch(form: YoutubeSearchForm):
    print("==============================", form.keyword)
    response = YoutubeClientApi.search(form.keyword)
    if response is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return response
    
@router.post("/twitter/search", response_model=dict)
async def twitterSearch(form: TwitterSearchForm):
    print("==============================", form.keyword)
    response = TwitterApi.search(form.keyword)
    if response is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return response