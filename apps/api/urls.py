from fastapi import APIRouter

from apps.api.crawler.urls import crawler_router

api = APIRouter()

api.include_router(crawler_router, tags=['crawler'], prefix='/crawler')
