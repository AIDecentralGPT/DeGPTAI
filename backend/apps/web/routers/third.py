from fastapi import APIRouter
from fastapi import Depends
from utils.utils import get_verified_user
from apps.web.api.tavily import TavilyClientInstance, TavilySearchForm
from apps.web.api.youtube import YoutubeClientInstance, YoutubeSearchForm


router = APIRouter()

@router.post("/tavily/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm):
    print("==============================", form.keyword)
    response = TavilyClientInstance.search(form.keyword)
    return response

@router.post("/youtube/search", response_model=dict)
async def youtubeSearch(form: YoutubeSearchForm):
    print("==============================", form.keyword)
    response = YoutubeClientInstance.search(form.keyword)
    return response