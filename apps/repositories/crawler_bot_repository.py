from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from apps.models.crawler import CrawlerBot


class CrawlerBotRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_bot(self, topic: str, group_id: str, status: int, social_id: int, server_id: int):
        bot = CrawlerBot(topic=topic, group_id=group_id,
                         status=status, social_id=social_id,
                         server_id=server_id)
        try:
            # Your database operation here
            self.db.add(bot)
            self.db.commit()
            self.db.refresh(bot)
        except IntegrityError as e:
            self.db.rollback()
            return None

        return bot

    def get_bot_by_id(self, bot_id: int):
        return self.db.query(CrawlerBot).filter(CrawlerBot.id == bot_id).first()

    def get_bot_by_group_id(self, group_id: str):
        return self.db.query(CrawlerBot).filter(CrawlerBot.group_id == group_id).first()

    def get_all_bots(self):
        return self.db.query(CrawlerBot).all()

    def check_exist_group_id(self, group_id):
        return self.db.query(func.count()).filter(CrawlerBot.group_id == group_id).scalar()

    def check_exist_id(self, id):
        return self.db.query(func.count()).filter(CrawlerBot.id == id).scalar()

    def update_bot_status(self, bot_id: int, new_status: int):
        bot = self.get_bot_by_id(bot_id)
        if bot:
            bot.status = new_status
            self.db.commit()
            self.db.refresh(bot)
        return bot

    def delete_bot(self, bot_id: int):
        bot = self.get_bot_by_id(bot_id)
        if bot:
            self.db.delete(bot)
            self.db.commit()
        return bot

    def get_bot_server_id(self, server_id):
        return (self.db.query(CrawlerBot).
                filter(CrawlerBot.server_id == server_id).all())
