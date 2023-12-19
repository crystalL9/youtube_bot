from typing import List

from fastapi import APIRouter
from fastapi_restful.cbv import cbv

from apps.api.crawler.schemas import CrawlerBotBaseCreate
from apps.models.crawler import Status
from apps.repositories.crawler_bot_repository import CrawlerBotRepository
from core.crawler_bot_worker import CrawlerBotFactory, active_bots, stop_consumer_flags
from core.custome_response import response
from core.database import db

bot_router = APIRouter()


@cbv(bot_router)
class BotApiView:
    @bot_router.post("/")
    async def create_bot(self, keywords: CrawlerBotBaseCreate):
        keywords = keywords
        group_id = keywords.group_id
        topic = keywords.topic
        social_id = keywords.social_id
        amount = keywords.amount
        server_id = keywords.server_id

        CrawlerBotFactory.create_topic_with_partitions(
                topic_name=topic,
                num_partitions=amount
        )

        for i in range(amount):
            bot = CrawlerBotRepository(db).create_bot(
                topic=topic,
                group_id=group_id,
                status=Status.ON.value,
                server_id=server_id,
                social_id=social_id
            )
            CrawlerBotFactory.start_bot_thread(topic, group_id, bot.id)

        return response(
            success=True,
            message="success",
            status_code=201
        )

    @bot_router.delete("/")
    async def delete_bot(self, ids: List[int]):
        success_ids = []
        error_ids = []
        for id in ids:
            try:
                bot = active_bots.pop(id)
                bot.stop()
                stop_consumer_flags[id] = True
                CrawlerBotRepository(db).delete_bot(id)
                success_ids.append(id)
            except Exception as e:
                error_ids.append(id)

        return response(
            success=True,
            message="success",
            data= {
                'deleted_bot_ids': success_ids,
                'failed_bot_ids': error_ids
            }
        )

    @bot_router.get("/list/")
    async def list_active_bots(self):
        active_bot_info = {}
        for id, bot in active_bots.items():
            active_bot_info[id] = {
                "topic": list(bot.consumer.subscription())[0],
                'id': id,
                'group_id': bot.group_id
            }
        return response(
            data=active_bot_info
        )

    # @bot_router.post("/run_script/"):
    #     pass
