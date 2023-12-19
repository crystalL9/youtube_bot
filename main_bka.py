import device_config_ultils
import json
import time
import threading
import itertools
import queue
from apps.api.crawler.youtube_crawler.utils import (
    DetailCrawler,
    HomePageCrawler,
    YoutubeUtil,
    StringHandler,
    GChromeDriver, InteractOption,
)
from apps.api.crawler.youtube_crawler.youtube_crawler import YoutubeCrawlerTool
from apps.api.crawler.youtube_crawler.utils import InteractOption
from apps.api.crawler.youtube_crawler.youtube_crawler import YoutubeCrawlerJob

# interact_option = InteractOption(
#         like_mode=False,
#         report_mode=False,
#         comment_mode=False,
#         comment_sample_list=["Ok", "Good content"],)

def search_key_word(queue_link):
    local_device_config = device_config_ultils.get_local_device_config()
    while True: 
        key_word_lists=eval(local_device_config[0]['mode']['keyword'].strip("[]"))
        for key_list in key_word_lists:
            mainkey=[]
            mainkey.append(key_list['key'])
        #  28/09/2023: Tìm kiếm và crawl video theo key chính và key phụ
            try:
                YoutubeCrawlerJob.get_link_search_key_word(
                username=local_device_config[0]['account']['username'],
                password=local_device_config[0]['account']['password'],
                main_key_list= mainkey,
                sub_key_list= None,
                queue_link=queue_link)
            except Exception as e:
                print(e)
                time.sleep(15*60)
                continue
def crawl_videos_keyword(link,tool):
    local_device_config = device_config_ultils.get_local_device_config()
    check=0
    while True: 
        key_word_lists=eval(local_device_config[0]['mode']['keyword'].strip("[]"))
        for key_list in key_word_lists:
            mainkey=[]
            mainkey.append(key_list['key'])
        #  28/09/2023: Tìm kiếm và crawl video theo key chính và key phụ
            try:
                YoutubeCrawlerJob.crawl_information_video(
                main_key= None,
                sub_key= None,
                link=link,
                tool=tool)
            except Exception as e:
                print(e)
                time.sleep(15*60)
                continue
            check=1

# def crawl_by_chanel(list_chanel):

    
#     local_device_config = device_config_ultils.get_local_device_config()
#     while True:
#         try: 
#             YoutubeCrawlerJob.run_script3(
#                         interact_option=interact_option,
#                         username=local_device_config[0]['account']['username'],
#                         password=local_device_config[0]['account']['password'],
#                         channel_urls=list_chanel
#                     )  
#         except:
#             time.sleep(15*60)
#             continue
# def crawl_by_chanel_long (list_chanel):

#     interact_option = InteractOption(
#         like_mode=False,
#         report_mode=False,
#         comment_mode=False,
#         comment_sample_list=["Ok", "Good content"],)
#     local_device_config = device_config_ultils.get_local_device_config()
#     while True:
#         try: 
#             YoutubeCrawlerJob.run_script10(
#                         interact_option=interact_option,
#                         username=local_device_config[0]['account']['username'],
#                         password=local_device_config[0]['account']['password'],
#                         channel_urls=list_chanel
#                     )  
#         except:
#             time.sleep(15*60)
#             continue
        
# def crawl_by_key():
#     interact_option = InteractOption(
#         like_mode=False,
#         report_mode=False,
#         comment_mode=False,
#         comment_sample_list=["Ok", "Good content"],)
#     local_device_config = device_config_ultils.get_local_device_config()
#     while True: 
#         key_word_lists=eval(local_device_config[0]['mode']['keyword'].strip("[]"))
#         for key_list in key_word_lists:
#             mainkey=[]
#             mainkey.append(key_list['key'])
#         #  28/09/2023: Tìm kiếm và crawl video theo key chính và key phụ
#             try:
#                 YoutubeCrawlerJob.run_script9(
#                 interact_option=interact_option,
#                 username=local_device_config[0]['account']['username'],
#                 password=local_device_config[0]['account']['password'],
#                 mainkey= mainkey,
#                 subkey= None)
#             except:
#                 time.sleep(15*60)
#                 continue

def chunk_list(lst, n):
    avg = len(lst) / float(n)
    out = []
    last = 0.0

    while last < len(lst):
        out.append(lst[int(last):int(last + avg)])
        last += avg

    return out

def read_lines_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


if __name__ == "__main__":
    local_device_config = device_config_ultils.get_local_device_config()
    username=local_device_config[0]['account']['username']
    password=local_device_config[0]['account']['password']
    tool = YoutubeCrawlerTool(username=username, password=password)
    queue_link_keyword=queue.Queue()
    #search_key_word(queue_link_keyword)
    crawl_videos_keyword('https://www.youtube.com/watch?v=NIpNzENBQvs',tool=tool)
    
    # các channel
    channel_urls = [ 
                        'https://www.youtube.com/@N10TV',
                        'https://www.youtube.com/@Tusachnhokhotanglon',
                        'https://www.youtube.com/@chienthangsuthat777',
                        'https://www.youtube.com/@Cuocsongmy22',
                        'https://www.youtube.com/@noiketnguoitinan',
                        'https://www.youtube.com/@tiengdan1010',
                        'https://www.youtube.com/@hQhTV',
                        'https://www.youtube.com/@tuoitrequocgia2610',
                        'https://www.youtube.com/@dieucaycaulacbonhabaotudo',
                        'https://www.youtube.com/@nhabaohanni',
                        'https://www.youtube.com/@TRELANGTV',
                        'https://www.youtube.com/@thongluan7747',
                        'https://www.youtube.com/@TAYNGUYEN24HTV',
                        'https://www.youtube.com/@TrucDienTV',
                        'https://www.youtube.com/@TMQ',
                        'https://www.youtube.com/@ThanhTTAD2',
                        'https://www.youtube.com/@TiViTuansanOnline',
                        'https://www.youtube.com/@JBNHVTV',
                        'https://www.youtube.com/@vietmediainaustralia9913',
                        'https://www.youtube.com/@luat-khoa',
                        'https://www.youtube.com/@henvoigiacmaa.cvoinhau5396',
                        'https://www.youtube.com/@nguyentiendung-bongoaigiao',
                        'https://www.youtube.com/@seanletv-tiengnoitudo',
                        'https://www.youtube.com/@BacHuTV',
                        'https://www.youtube.com/@PhilDong',
                        'https://www.youtube.com/@tanthai7336',
                        'https://www.youtube.com/@vietnewstelevision',
                        'https://www.youtube.com/@VanHoaNBLV1',
                        'https://www.youtube.com/@Vietnamtvnews'
                        'https://www.youtube.com/@tincongdong2559'
                        ]
    channel_urls_long=[
                        'https://www.youtube.com/@thoibao-de',
                        'https://www.youtube.com/@NguoiYeuNuocViet',
                        'https://www.youtube.com/@TamThucVietAnhChi',
                        'https://www.youtube.com/@VOATiengViet',
                        'https://www.youtube.com/@SBTNOfficial',
                        'https://www.youtube.com/@VietTan',
                        'https://www.youtube.com/@VIETLIVETV' 
                        ]

    
   # channel_chunks = chunk_list(channel_urls, 2)
    # crawl theo list channel
    # thread1 = threading.Thread(target=crawl_by_chanel, args=(channel_chunks[0],))
    # thread2 = threading.Thread(target=crawl_by_chanel, args=(channel_chunks[1],))
    #thread4 = threading.Thread(target=crawl_by_chanel_long, args=(channel_urls_long,))
    # thread5 = threading.Thread(target=crawl_by_key)
    # thread6 = threading.Thread(target=crawl_by_chanel, args=(channel_crawled_array,))


    # thread1.start()
    # thread2.start()
    #thread4.start()
    # thread5.start()
    # thread6.start()

    # thread1.join()
    # thread2.join()
    #thread4.join()
    # thread5.join()
    # thread6.start()
