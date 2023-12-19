import signal
import sys

from apps.models.crawler import CrawlerBot
from core.database import db


# Đăng ký signal handler
def clean_crawl_bot_data(signum, frame):
    print("Ctrl+C detected. Cleaning up...")
    db.query(CrawlerBot).delete()  # Xoá toàn bộ dữ liệu trong bảng
    db.commit()
    sys.exit(0)


signal.signal(signal.SIGINT, clean_crawl_bot_data)

# Chạy ứng dụng chính của bạn ở đây
