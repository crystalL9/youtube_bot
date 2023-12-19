from fastapi import APIRouter

from apps.api.crawler.views import bot_router

crawler_router = APIRouter()
crawler_router.include_router(bot_router, prefix='/bot')
