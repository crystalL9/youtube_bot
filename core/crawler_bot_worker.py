import json
import threading

from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic

from apps.api.crawler.youtube_crawler.utils import InteractOption
from apps.api.crawler.youtube_crawler.youtube_crawler import YoutubeCrawlerJob
from apps.repositories.crawler_bot_repository import CrawlerBotRepository
from core.database import db

KAFKA_SERVER_URL = 'localhost:9092'
OFFSET_FILTER = 'earliest'
active_bots = {}
active_threads = {}
stop_consumer_flags = {}


class SocialTool:
    TOOL_OPTION = {
        'YOUTUBE': YoutubeCrawlerJob,
        'TIKTOK': 'TiktokPseudo',
        'FACEBOOK': 'FacebookPseudo',
    }


class CrawlerBot:

    def __init__(self, topic, group_id, id):
        self.consumer = KafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=KAFKA_SERVER_URL,
            auto_offset_reset=OFFSET_FILTER,
            enable_auto_commit=True,
            value_deserializer=lambda x: self.deserialize_message(x)
        )
        self.topic = topic
        self.group_id = group_id
        self.id = id
        self.current_script = None
        self.current_params = None

    def deserialize_message(self, value):
        try:
            return json.loads(value.decode('utf-8'))
        except json.JSONDecodeError as e:
            print(f"Error decoding message: {e}")
            return None

    def run(self):
        for message in self.consumer:
            if stop_consumer_flags.get(self.id):
                break
            print(f'Bot {self.id}: {message.value}')
            # try:
            #     interact_option = InteractOption(
            #         like_mode=False,
            #         report_mode=False,
            #         comment_mode=False,
            #         comment_sample_list=["Ok", "Good content"],
            #     )
            #     SocialTool.TOOL_OPTION['YOUTUBE']()['run_script6'](
            #         username="ncs.crawler.bot@gmail.com",
            #         password="an845919",
            #         interact_option=interact_option,
            #         hashtag_list=["Amee", "Bray"]
            #     )
            # except BaseException as e:
            #     continue

    def stop(self):
        self.consumer.close()


class CrawlerBotFactory:
    @staticmethod
    def create_bot(topic, group_id, id):
        crawl_bot = CrawlerBot(topic,
                               group_id,
                               id)
        active_bots[id] = crawl_bot
        stop_consumer_flags[id] = False
        crawl_bot.run()

    @staticmethod
    def start_bot_thread(topic, group_id, id):
        bot_thread = threading.Thread(target=CrawlerBotFactory.create_bot,
                                      args=(topic, group_id, id))
        active_threads[id] = bot_thread
        bot_thread.start()

    @staticmethod
    def create_topic_with_partitions(topic_name, num_partitions=10,
                                     replication_factor=1,
                                     bootstrap_servers=KAFKA_SERVER_URL):
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
            new_topic = NewTopic(name=topic_name, num_partitions=num_partitions,
                                 replication_factor=replication_factor)
            admin_client.create_topics(new_topics=[new_topic])
            admin_client.close()
            return True
        except Exception as e:
            return False

    @staticmethod
    def back_up_init(server_id):
        bots = CrawlerBotRepository(db).get_bot_server_id(server_id)

        for bot in bots:
            CrawlerBotFactory.start_bot_thread(bot.topic,
                                               bot.group_id,
                                               bot.id)
