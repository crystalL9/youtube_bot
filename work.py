import device_config_ultils
import time
import threading
import queue
from apps.api.crawler.youtube_crawler.youtube_crawler import YoutubeCrawlerTool
from apps.api.crawler.youtube_crawler.youtube_crawler import YoutubeCrawlerJob
from elasticsearch import Elasticsearch
from datetime import timedelta,datetime
import datetime as dt
from logger import Colorlog

queue_lock = threading.Lock()
tool_lock = threading.Lock()

def search_key_word(queue_link,tool,max_size_post):
    local_device_config = device_config_ultils.get_local_device_config()
    while True:
        with queue_lock:
            key_word_lists=local_device_config[0]['mode']['keyword']
            max_size_post= local_device_config[0]['mode']['max_size_post']
            with tool_lock:
                try:
                        YoutubeCrawlerJob.get_link_search_key_word(
                        # username=local_device_config[0]['account']['username'],
                        # password=local_device_config[0]['account']['password'],
                        # username=None,
                        # password=None,
                        main_key_list= key_word_lists,
                        sub_key_list= None,
                        queue_link=queue_link,
                        tool=tool,
                        max_size_post=max_size_post)
                except Exception as e:
                        time.sleep(15*60)
                        continue
def search_channel(queue_link,tool,list_channel,max_size_post):
    while True: 
            with queue_lock and tool_lock:
                try:
                    YoutubeCrawlerJob.get_link_search_channel(
                        tool=tool,
                        queue_link=queue_link,
                        list_link_channels=list_channel,
                        max_size_post=max_size_post
                        )
                except Exception as e:
                    time.sleep(15*60)
                    continue
def crawl_videos(queue_link, tool,mode):
    while True:
        try:
            link = queue_link.get(timeout=10)
            if 'shorts'in link:
                continue
        except queue.Empty:
            log_white("Hàng đợi trống.")
            time.sleep(10)
            continue

        # 28/09/2023: Tìm kiếm và crawl video theo key chính và key phụ
        try:
            YoutubeCrawlerJob.crawl_information_video(
                main_key=None,
                sub_key=None,
                link=link,
                tool=tool,
                mode=mode
            )
        except Exception as e:
            print(e)
            time.sleep(15*60)
            continue
        finally:
            queue_link.task_done()

def crawl_videos_update(queue_link, tool,mode,time_start_upate):
    check = False
    while True:
        print(f'Chờ đến  {time_start_upate} để thực hiện cập nhật')
        start_time = datetime.datetime.strptime(time_start_upate, "%H:%M:%S")
        end_time = start_time - datetime.timedelta(minutes=5)
        current_time = dt.datetime.now().strftime("%H:%M:%S")
        if current_time >= end_time and current_time < time_start_upate:
            check = False
        if current_time==time_start_upate:
            print(f'Bắt đầu thực hiện cập nhật')
            check=True
        try:
            link = queue_link.get(timeout=10)
            if 'shorts'in link:
                continue
        except queue.Empty:
            time.sleep(10)
            continue

        # 28/09/2023: Tìm kiếm và crawl video theo key chính và key phụ
        try:
            YoutubeCrawlerJob.crawl_information_video_update(
                main_key=None,
                sub_key=None,
                link=link,
                tool=tool,
                mode=mode,
                check=check
            )
        except Exception as e:
            print(e)
            time.sleep(15*60)
            continue
        finally:
            queue_link.task_done()
def read_lines_from_file(url,mode):
    if mode ==1:
        try:
            with open('error/error_link.txt', 'r') as file:
                lines = file.readlines()
        except:
            lines=[]
    if mode ==2:
        try:
            with open(f'error/{str(url).split("/")[-1]}_error.txt', 'r') as file:
                lines = file.readlines()
        except:
            lines=[]
    return lines
def read_lines_from_file_done(url,mode):
    if mode ==1:
        try:
            with open('link_crawled/crawled.txt', 'r') as file:
                lines = file.readlines()
        except:
            lines=[]
    if mode ==2:
        try:
            with open(f'link_crawled/{str(url).split("/")[-1]}.txt', 'r') as file:
                lines = file.readlines()
        except:
            lines=[]
    return lines

def work_keyword(local_device_config):
    options_list=local_device_config[0]['listArgument']
    max_size_post=local_device_config[0]['mode']['max_size_post']
    while True:
        try:
            username=None
            password=None
            queue_link_channel_long = queue.Queue()
           
            try:
                tool3 = YoutubeCrawlerTool(options_list=options_list,username=username, password=password)      
                search_channel_long_thread = threading.Thread(target=search_key_word, args=(queue_link_channel_long,tool3))
                search_channel_long_thread.start()
                tool4  = YoutubeCrawlerTool(options_list=options_list,username=username, password=password) 
                crawl_thread4 = threading.Thread(target=crawl_videos, args=(queue_link_channel_long, tool4,1))
                crawl_thread4.start()
                search_channel_long_thread.join()
                crawl_thread4.join()
            except:
                pass   
        except:
            time.sleep(4)
            continue

def work1(local_device_config):
    options_list=local_device_config[0]['listArgument']
    channel_urls=local_device_config[0]['mode']['channel_link']
    max_size_post=local_device_config[0]['mode']['max_size_post']
    while True:
        try:
            # username = local_device_config[0]['account']['username']
            # password = local_device_config[0]['account']['password']
            username=None
            password=None
            queue_link_channel_long2 = queue.Queue()
            try:
                tool4  = YoutubeCrawlerTool(options_list=options_list,username=username, password=password)      
                search_channel_long_thread2 = threading.Thread(target=search_channel, args=(queue_link_channel_long2,tool4,channel_urls,max_size_post))
                search_channel_long_thread2.start()
                
            except: 
                pass
            try:
                tool6  = YoutubeCrawlerTool(options_list=options_list,username=username, password=password) 
                crawl_thread6 = threading.Thread(target=crawl_videos, args=(queue_link_channel_long2, tool6,2))
                crawl_thread6.start()
            except:
                pass
            try:
                tool7  = YoutubeCrawlerTool(options_list=options_list,username=username, password=password) 
                crawl_thread7 = threading.Thread(target=crawl_videos, args=(queue_link_channel_long2, tool7,2))
                crawl_thread7.start()
            except:
                pass
            #Chờ cho tất cả các item trong hàng đợi được xử lý xong
            search_channel_long_thread2.join()
            crawl_thread6.join()
            crawl_thread7.join()
            for url in channel_urls:
                queue_link_channel_long_error = queue.Queue()
                lines=read_lines_from_file(url=url,mode=2)
                done=read_lines_from_file_done(url=url,mode=2)
                if lines:
                    for line in lines:
                        if line not in done:
                            queue_link_channel_long_error.put(f'thttps://www.youtube.com/watch?v={line}')
                else:
                    continue
            try: 
                tool8 = tool3 = YoutubeCrawlerTool(options_list=options_list,username=username, password=password)     
                crawl_videos(queue_link_channel_long_error, tool8,2)
                tool8.driver.quit()
            except:
                pass   
        except:
            time.sleep(4)
            continue
def get_link(queue_link,gte,lte):
    es = Elasticsearch(["http://192.168.143.54:9200"])
    body1 = {
            "query": {
                "bool": {
                "must": [
                    {
                    "match": {
                        "type.keyword": "youtube video"
                    }
                    },
                    {
                    "bool": {
                        "filter": {
                        "range": {
                            "time_crawl": {
                            "gte": f"{gte}",
                            "lte": f"{lte}",
                            "format": "yyyy/MM/dd HH:mm:ss"
                            }
                        }
                        }
                    }
                    }
                ]
                }
            },
            "sort": [
                {"_id": "desc"}
            ]
}
    # Lấy kết quả đầu tiên
    result = es.search(index="osint_posts", body=body1)
    dataFramse_Log = []
    for result_source in result['hits']['hits']:
        dataFramse_Log.append(result_source)
    # Lấy kết quả tiếp theo bằng cách sử dụng search_after
    while len(result["hits"]["hits"]) > 0:
        last_hit = result["hits"]["hits"][-1]
        body1["search_after"] = [last_hit["_id"]]
        result = es.search(index="osint_posts", body=body1)
        for result_source in result['hits']['hits']:
            dataFramse_Log.append(result_source)
    for item in dataFramse_Log:
            print(f'Put: {item["_source"]["link"]} to Queue')
            queue_link.put(item["_source"]["link"])
    es.close()
   
def get_link_es(queue,time_start_upate,range_date):
    while True:

        current_time = dt.datetime.now().strftime("%H:%M:%S")
        if current_time == time_start_upate:
            queue.queue.clear()
            print(f' Thời gian hiện tại là  {time_start_upate}. Bắt đầu thực hiện cập nhật')    
            current_date = datetime.now()
            one_day_ago = current_date - timedelta(days=int(range_date[0]))
            formatted_date = current_date.strftime("%Y/%m/%d")
            one_day_ago_formatted_date=one_day_ago.strftime("%Y/%m/%d")
            six_day_ago = current_date - timedelta(days=int(range_date[1]-1))
            seven_day_ago = current_date - timedelta(days=int(range_date[1]))
            six_day_ago_formatted_date=six_day_ago.strftime("%Y/%m/%d")
            seven_day_ago_formatted_date=seven_day_ago.strftime("%Y/%m/%d")
            print(f"💻💻💻 Bắt đầu lấy link của ngày {one_day_ago_formatted_date} và ngày {seven_day_ago_formatted_date}")
            gte=f'{one_day_ago_formatted_date} 00:00:00'
            lte=f'{formatted_date} 00:00:00'
            try:
                get_link(queue_link=queue,gte=gte,lte=lte)
            except:
                pass
            time.sleep(30)
            gte=f'{seven_day_ago_formatted_date} 00:00:00'
            lte=f'{six_day_ago_formatted_date} 00:00:00'
            try:
                get_link(queue_link=queue,gte=gte,lte=lte)
            except:
                pass
            print(f" ☑ ☑ ☑ Đã lấy hết link của ngày {one_day_ago_formatted_date} và ngày {seven_day_ago_formatted_date} ")
        else:
            yellow_color = "\033[93m"
            reset_color = "\033[0m"
            print(f'{yellow_color}{dt.datetime.now()} *** UPDATE TOOL : Chờ đến  {time_start_upate} để bắt đầu thực hiện cập nhật{reset_color}')
            continue

def update(local_device_config):
    options_list=local_device_config[0]['listArgument']
    time_start_upate=local_device_config[0]['mode']['start_time_run']
    range_date=local_device_config[0]['mode']['range_date']
    queue_link_update = queue.Queue()

    crawl_thread5 = threading.Thread(target=get_link_es, args=(queue_link_update,time_start_upate,range_date))
    crawl_thread5.start()
    # username = local_device_config[0]['account']['username']
    # password = local_device_config[0]['account']['password']
    username = None
    password = None

    tool6 = YoutubeCrawlerTool(options_list=options_list,username=username, password=password) 
    crawl_thread6 = threading.Thread(target=crawl_videos_update, args=(queue_link_update, tool6,3,time_start_upate))
    crawl_thread6.start()

    tool7 = YoutubeCrawlerTool(options_list=options_list,username=username, password=password) 
    crawl_thread7 = threading.Thread(target=crawl_videos_update, args=(queue_link_update, tool7,3,time_start_upate))
    crawl_thread7.start()
    crawl_thread5.join()
    crawl_thread6.join()
    crawl_thread7.join()

def test(local_device_config):   
        try:
            # username = local_device_config[0]['account']['username']
            # password = local_device_config[0]['account']['password']
            options_list=local_device_config[0]['mode']['listArgument']
            username=None
            password=None
            queue_link_channel_long = queue.Queue()
            queue_link_channel_long.put('https://www.youtube.com/watch?v=8uV9xaWaETM')
            # try:
            #     tool3 = YoutubeCrawlerTool(username=username, password=password)      
            #     search_channel_long_thread = threading.Thread(target=search_channel_long, args=(queue_link_channel_long,tool3,channel_urls))
            #     search_channel_long_thread.start()
            # except: 
            #     pass
            try:
                tool4 = YoutubeCrawlerTool(options_list=options_list,username=username, password=password)
                crawl_thread4 = threading.Thread(target=crawl_videos, args=(queue_link_channel_long, tool4,2))
                crawl_thread4.start()
            except:
                pass
            # try: 
            #     tool5 = YoutubeCrawlerTool(username=username, password=password)      
            #     crawl_thread5 = threading.Thread(target=crawl_videos, args=(queue_link_channel_long, tool5,2))
            #     crawl_thread5.start()
            # except:
            #      pass
            # try: 
            #     tool7 = YoutubeCrawlerTool(username=username, password=password)      
            #     crawl_thread7 = threading.Thread(target=crawl_videos, args=(queue_link_channel_long, tool7,2))
            #     crawl_thread7.start()
            # except:
            #      pass
            # Chờ cho tất cả các item trong hàng đợi được xử lý xong
            #search_channel_long_thread.join()
            crawl_thread4.join()
            #crawl_thread5.join()
            # crawl_thread7.join()
            # for url in channel_urls:
            #     queue_link_channel_long_error = queue.Queue
            #     lines=read_lines_from_file(url=url,mode=2)
            #     done=read_lines_from_file_done(url=url,mode=2)
            #     if lines:
            #         for line in lines:
            #             if line not in done:
            #                 queue_link_channel_long_error.put(line)
            #     else:
            #         continue
            # try: 
            #     tool6 = YoutubeCrawlerTool(username=username, password=password)      
            #     crawl_videos(queue_link_channel_long, tool6,2)
            #     tool6.driver.quit()
            # except:
            #     pass   
        except Exception as e:
            print(e)
            time.sleep(4)
