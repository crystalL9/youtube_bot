# from pydantic import BaseModel, validator
#
from pydantic import BaseModel


class CrawlerBotBase(BaseModel):
    topic: str
    group_id: str
    social_id: int


class CrawlerBotBaseCreate(CrawlerBotBase):
    amount: int
    server_id: int


class CrawlerBot(CrawlerBotBase):
    id: int

    class Config:
        from_attributes = True


class InputScriptConfig:
    pass
