import time
from pytube import YouTube
from selenium.webdriver.common.by import By
from apps.api.crawler.utils.crawler_logger import CrawlerLogger
from .utils import (
    DetailCrawler,
    HomePageCrawler,
    YoutubeUtil,
    StringHandler,
    GChromeDriver, InteractOption,
)

YOUTUBE_HOMEPAGE_URL = "https://www.youtube.com"
BROWSER_LANGUAGE = "en"
HASHTAG_SEARCH_URL = "https://www.youtube.com/hashtag"

crawler_logger = CrawlerLogger()


class YoutubeCrawlerTool:
    def __init__(self, options_list,username=None, password=None):
        self.driver = GChromeDriver.init_driver(options_list,username, password)
        self.detail_crawler = DetailCrawler(self.driver)
        self.string_handler = StringHandler
        self.homepage_crawler = HomePageCrawler(self.driver)
        self.util = YoutubeUtil(self.driver)
        username = username
        password = password
    
    # tab chrome để lấy link search theo keyword
    def get_link_search_key_word(self,sub_key_list,main_key_list,queue_link,max_size_post):
        while True:
            crawled_video_links = self.read_file_lines('link_crawled/crawled.txt')
            if sub_key_list!=None:
                for mainkey in main_key_list:
                    for subkey in sub_key_list:
                        # kết quả tìm kiếm được sắp xếp theo ngày đăng
                        search_url = f'https://www.youtube.com/results?search_query="{mainkey}""{subkey}"&sp=CAI%253D'
                        self.driver.get(search_url)
                        time.sleep(3)
                        video_links=self.extract_link_from_page(crawled_link=crawled_video_links,queue_link=queue_link,max_size_post=max_size_post)
                        if len(video_links)!=0:
                            for link in reversed(video_links):
                                queue_link.put(link)
                print("******** Search hết bộ keyword, tạm dừng chờ video mới *********")
                self.driver.get('about:blank')
                time.sleep(3600*2)    

            elif sub_key_list==None:
                    for mainkey in main_key_list:
                        print(f'================= Tìm kiếm với từ khóa "{mainkey}" ================= ')
                        # kết quả tìm kiếm được sắp xếp theo ngày đăng
                        search_url = f'https://www.youtube.com/results?search_query="{mainkey}"&sp=CAI%253D'
                        self.driver.get(search_url)
                        time.sleep(3)
                        video_links=self.extract_link_from_page(crawled_link=crawled_video_links,queue_link=queue_link,max_size_post=max_size_post)
                        if len(video_links)!=0:
                            for link in reversed(video_links):
                                queue_link.put(link)
                    print("******** Search hết bộ keyword, tạm dừng chờ video mới *********")
                    self.driver.get('about:blank')
                    time.sleep(3600*2)
            
    # tab chrome để lấy link search theo channel
    def get_link_search_channel(self,queue_link,list_link_channels,max_size_post):
        while True:
            for link_channel in list_link_channels:
                id_channel=link_channel.split('/')[-1]
                try:
                    crawled_video_links = self.read_file_lines(f'link_crawled/{id_channel}.txt')
                except:
                    crawled_video_links = []

                try:
                    self.driver.get(f'{link_channel}/videos')
                    time.sleep(3)
                    video_links=self.extract_link_from_channel(crawled_link=crawled_video_links,queue_link=queue_link,max_size_post=max_size_post)
                    if len(video_links)!=0:
                        for link in reversed(video_links):
                            queue_link.put(link)
                    time.sleep(3)
                except:
                    pass
                try:
                    self.driver.get(f'{link_channel}/streams')
                    time.sleep(3)
                    video_links=self.extract_link_from_channel(crawled_link=crawled_video_links,queue_link=queue_link,max_size_post=max_size_post)
                    if len(video_links)!=0:
                        for link in reversed(video_links):
                            queue_link.put(link)
                    time.sleep(3)
                except:
                    pass
            print("******** Search hết các video hiện tại, tạm dừng chờ video mới *********")
            self.driver.get('about:blank')
            time.sleep(3600*2)
            

    # tab chrome để lấy link search theo channel (cho channel siêu nhiều video để demo :)))
    def get_link_search_channel_long(self,queue_link,list_link_channels):
        while True:
            for link in list_link_channels:
                id_channel=link.split('/')[-1]
                try:
                    crawled_video_links = self.read_file_lines(f'link_crawled/{id_channel}.txt')
                except:
                    crawled_video_links = []

                try:
                    self.driver.get(f'{link}/videos')
                    time.sleep(3)
                    video_links=self.extract_link_from_channel_long(crawled_link=crawled_video_links,queue_link=queue_link)
                    if len(video_links)!=0:
                        for link in reversed(video_links):
                            queue_link.put(link)
                    time.sleep(3)
                except:
                    pass
                try:
                    self.driver.get(f'{link}/streams')
                    time.sleep(3)
                    video_links=self.extract_link_from_channel_long(crawled_link=crawled_video_links,queue_link=queue_link)
                    if len(video_links)!=0:
                        for link in reversed(video_links):
                            queue_link.put(link)
                    time.sleep(3)
                except:
                    pass
            print("******** Search hết các video hiện tại, tạm dừng chờ video mới *********")
            self.driver.get('about:blank')
            time.sleep(3600*2)
   ######################################################################

   # Đọc file ra list
    def read_file_lines(self,file_path):
        lines = []
        with open(file_path, 'r') as file:
            for line in file:
                lines.append(line.strip())
        return lines
    
    # Xử lý để lấy link gốc
    def excute_link(self,link):
        if '&' in link:
            link = link.split('&')[0]
        return link
    # Lưu các link đã crawl ra file
    def save_array_to_txt(self, arr, file_path):
        with open(file_path, 'a') as file:
            for element in arr:
                file.write(str(element))
                file.write('\n')
    # 28/09/2023: Tìm kiếm theo key chính và key phụ
    def search_video_by_mainkey(self, interact_option,main_key_list,sub_key_list):
        # Đọc từ file ra các link đã crawled --> list
        if sub_key_list!=None:
            for mainkey in main_key_list:
                for subkey in sub_key_list:
                    # split_mainkey= '""'.join(mainkey.split())
                    # split_subkey= '""'.join(subkey.split())
                    crawled_video_links = self.read_file_lines('link_crawled/crawled.txt')
                    # kết quả tìm kiếm được sắp xếp theo ngày đăng
                    search_url = f'https://www.youtube.com/results?search_query="{mainkey}""{subkey}"&sp=CAI%253D'
                    self.driver.get(search_url)
                    crawled=self._crawled_data_in_search_screen(interact_option,
                                                            keyword = None, crawled_video_links = crawled_video_links,
                                                            main_key = mainkey, sub_key= subkey)
        elif sub_key_list==None:
                for mainkey in main_key_list:
                    crawled_video_links = self.read_file_lines('link_crawled/crawled.txt')
                    # kết quả tìm kiếm được sắp xếp theo ngày đăng
                    search_url = f'https://www.youtube.com/results?search_query="{mainkey}"&sp=CAI%253D'
                    self.driver.get(search_url)
                    crawled=self._crawled_data_in_search_screen(interact_option,
                                                            keyword = None, crawled_video_links = crawled_video_links,
                                                            main_key = mainkey, sub_key= None)
                    

    def channel_url_scrape_video(self, video_links, channel_url):
        data_by_channel_dict = {channel_url: []}
        for index, video_link in enumerate(video_links):
            try:
                data_by_channel_dict[channel_url].append(
                    self.detail_crawler.run(video_link)
                )
                crawler_logger.info(
                    f"Processing keyword: {channel_url} ({index + 1}/{len(video_links)})"
                )
            except Exception as e:
                crawler_logger.error(str(e))
        return data_by_channel_dict

    def crawl_information_video(self,video_link, main_key, sub_key,mode):
        crawled_data_list = []
        try:
            crawl_data = self.detail_crawler.run(
                video_url=video_link,
                main_key=main_key,
                sub_key=sub_key,
                mode=mode
            )
            if crawl_data:
                video_detail, comments = crawl_data
                crawled_data_list.append(video_detail)
                crawled_data_list.extend(comments)
        except Exception as e:
            crawler_logger.error(str(e))
        return crawled_data_list

    def report_video(self, video_link):
        self.driver.maximize_window()
        self.driver.get(video_link)
        time.sleep(2)
        self.util.report()

    def _scrape_videos_by_keyword(self, keyword, interact_option):
        self.driver.minimize_window()
        format_keyword = "+".join(keyword.split())

        # kết quả tìm kiếm được sắp xếp theo ngày đăng
        search_url = f"https://www.youtube.com/results?search_query={format_keyword}&sp=CAI%253D"
        self.driver.get(search_url)
        #self.util.recently_click()
        return self._crawled_data_in_search_screen(interact_option,
                                                   keyword)

    def _scrape_videos_by_channel(self, channel_url,
                                  interact_option):
        self.driver.minimize_window()
        id_channel= str(channel_url).split('/')[3]
        crawled_video_links = []
        with open('link_crawled/links_crawled_in_channels.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith(f'{id_channel}.'):
                    link_parts = line.strip().split('.')
                    link = '.'.join(link_parts[1:])
                    crawled_video_links.append(link)
        self.driver.get(f'{channel_url}/videos')
        time.sleep(3)
        return self._crawled_data_in_thumbnails_screen(interact_option,crawled_video_links,id_chanel=id_channel)
    
    # test lấy 1000 video của các kênh có quá nhiều video để demo
    def _scrape_videos_by_channel_long(self, channel_url,
                                  interact_option):
        id_channel= str(channel_url).split('/')[3]
        crawled_video_links = []
        with open('link_crawled/links_crawled_in_channels_long.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith(f'{id_channel}.'):
                    link_parts = line.strip().split('.')
                    link = '.'.join(link_parts[1:])
                    crawled_video_links.append(link)
        self.driver.get(f'{channel_url}/videos')
        time.sleep(3)
        return self._crawled_data_in_thumbnails_screen_long(interact_option,crawled_video_links,id_chanel=id_channel)
    
    def save_link(self, txt, file_path):
        with open(file_path, 'a') as file:
                file.write(txt)
                file.write('\n')
    def crawl_information_video_2(self, interact_option, keyword, crawled_video_links, main_key, sub_key):
        can_scroll = True
        check = 0
        while can_scroll:
            if check != 0:
                if len(video_links) == 0:
                    can_scroll = False
                    continue

            video_links = self.extract_link_from_page(crawled_link=crawled_video_links)
            if video_links is None:
                video_links = []
        
            try:
                for link in reversed(video_links.copy()):
                    link_short=self.excute_link(link)
                    if 'shorts' in link_short:
                        if video_links is not None:
                            video_links.remove(link)
                        continue
                    if link_short in crawled_video_links:
                        if video_links is not None:
                            video_links.remove(link)
                        continue
                    data = self.scrape_video_by_links(
                        interact_option = interact_option,
                        video_links = link_short,
                        keyword = None,
                        main_key= main_key,
                        sub_key= sub_key
                        )
                    self.save_link(link_short,'link_crawled/crawled.txt')
                    if video_links is not None:
                        video_links.remove(link)
            except Exception as e:
                if video_links is not None:
                    video_links.remove(link)
                with open("error/error_link.txt", "a") as file:
                    file.write(link)
                    file.write('\n')
                crawler_logger.error(str(e))

            check += 1
            time.sleep(5)
        return crawled_video_links
    
# 11/10/2023 update code mới 
    def _crawled_data_in_thumbnails_screen(self, interact_option,crawled_video_links,id_chanel):
        self.driver.minimize_window()
        can_scroll = True
        check = 0
        while can_scroll:
            if check != 0:
                if len(video_links) == 0:
                    can_scroll = False
                    continue

            video_links = self.extract_link_from_channel(crawled_link=crawled_video_links)
            if video_links is None:
                video_links = []
                return crawled_video_links
        
            try:
                for link in reversed(video_links.copy()):
                    link_short=self.excute_link(link)
                    if 'shorts' in link_short:
                        if video_links is not None:
                            video_links.remove(link)
                        continue
                    if link_short in crawled_video_links:
                        if video_links is not None:
                            video_links.remove(link)
                        continue
                    data = self.scrape_video_by_links(
                        interact_option = interact_option,
                        video_links = link_short,
                        keyword = None,
                        main_key= None,
                        sub_key= None
                        )
                    self.save_link(f'{id_chanel}.{link_short}','link_crawled/links_crawled_in_channels.txt')
                    if video_links is not None:
                        video_links.remove(link)
            except Exception as e:
                if video_links is not None:
                    video_links.remove(link)
                with open("error/error_link.txt", "a") as file:
                    file.write(link)
                    file.write('\n')
                crawler_logger.error(str(e))

            check += 1
            time.sleep(5)
        return crawled_video_links
    

    def _crawled_data_in_thumbnails_screen_long(self, interact_option,crawled_video_links,id_chanel):
        can_scroll = True
        check = 0
        while can_scroll:
            if check != 0:
                if len(video_links) == 0:
                    can_scroll = False
                    continue

            video_links = self.extract_link_from_channel_long(crawled_link=crawled_video_links)
            if video_links is None:
                video_links = []
                return crawled_video_links
        
            try:
                for link in reversed(video_links.copy()):
                    link_short=self.excute_link(link)
                    if 'shorts' in link_short:
                        if video_links is not None:
                            video_links.remove(link)
                        continue
                    if link_short in crawled_video_links:
                        if video_links is not None:
                            video_links.remove(link)
                        continue
                    data = self.scrape_video_by_links(
                        interact_option = interact_option,
                        video_links = link_short,
                        keyword = None,
                        main_key= None,
                        sub_key= None
                        )
                    self.save_link(f'{id_chanel}.{link_short}','link_crawled/links_crawled_in_channels_long.txt')
                    if video_links is not None:
                        video_links.remove(link)
            except Exception as e:
                if video_links is not None:
                    video_links.remove(link)
                with open("error/error_link.txt", "a") as file:
                    file.write(link)
                    file.write('\n')
                crawler_logger.error(str(e))

            check += 1
            time.sleep(5)
        return crawled_video_links

    def link_to_id(self,link):
        yt = YouTube(link)
        video_id = yt.video_id
        return video_id
        
    def extract_link_from_page(self,crawled_link,queue_link,max_size_post):
        video_links=[]
        while True:
            before_scroll_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            time.sleep(3)
            after_scroll_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            video_title_elements = self.driver.find_elements(By.XPATH, '//a[@id="video-title"]')
            reversed_elements = video_title_elements
            for element in reversed_elements:
                link= self.excute_link(element.get_attribute("href"))
                id=self.link_to_id(link)
                if id in video_links:
                    pass
                elif id in crawled_link:
                        return video_links
                else:
                        video_links.append(link)
            if after_scroll_height == before_scroll_height:
                return video_links
            if max_size_post > 0 :
                if len(video_links) == int(max_size_post):
                    return video_links
                else:
                    pass

            
    
    #  11/10/2023 tìm kiếm link trong channel
    # def extract_link_from_channel(self,crawled_link):
    #     self.driver.minimize_window()
    #     video_links=[]
    #     time.sleep(4)
    #     self.scroll_down()
    #     video_title_elements = self.driver.find_elements(By.XPATH, '//*[@id="thumbnail"]/ytd-thumbnail/a')
    #     for element in video_title_elements:
    #         link= self.excute_link(element.get_attribute("href"))
    #         if link in crawled_link:
    #             return video_links
    #         else:
    #             video_links.append(link)
    #     return video_links
    def extract_link_from_channel(self,crawled_link,queue_link,max_size_post):
        video_links=[]
        id_video=[]
        while True:
            before_scroll_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(3)
            after_scroll_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            video_title_elements = self.driver.find_elements(By.XPATH, '//*[@id="thumbnail"]/ytd-thumbnail/a')
            for element in video_title_elements:
                link= self.excute_link(element.get_attribute("href"))
                id=self.link_to_id(link)
                if id in id_video:
                    pass
                elif id in crawled_link:
                        return video_links
                else:
                        id_video.append(id)
                        video_links.append(link)
                        
            if after_scroll_height == before_scroll_height:
                return video_links
            if max_size_post > 0 :
                if len(video_links) == int(max_size_post):
                    return video_links
                else:
                    pass
            
    def extract_link_from_channel_long(self,crawled_link,queue_link):
        video_links=[]
        while True:
            if len(video_links)>500:
                return video_links
            before_scroll_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(5)
            after_scroll_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            video_title_elements = self.driver.find_elements(By.XPATH, '//*[@id="thumbnail"]/ytd-thumbnail/a')
            for element in video_title_elements:
                link= self.excute_link(element.get_attribute("href"))
                if link in video_links:
                    pass
                elif link in crawled_link:
                        return video_links
                else:
                        video_links.append(link)
            if after_scroll_height == before_scroll_height:
                return video_links
            
    def scroll_down(self):
        while True:
            before_scroll_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(5)
            after_scroll_height = self.driver.execute_script("return document.documentElement.scrollHeight")

            if after_scroll_height == before_scroll_height:
                break

class YoutubeCrawlerJob:
    def __init__(self):
        pass

    def __getitem__(self, key):
        if hasattr(self, key) and callable(getattr(self, key)):
            return lambda *args, **kwargs: getattr(self, key)(*args, **kwargs)
        else:
            raise KeyError(f"Method '{key}' not found")
    
    @staticmethod
    def get_link_search_key_word(sub_key_list,main_key_list,queue_link,tool,max_size_post):
        tool.get_link_search_key_word(main_key_list=main_key_list,sub_key_list=sub_key_list,queue_link=queue_link,max_size_post=max_size_post)
        tool.driver.get('about:blank')
        
    @staticmethod
    def crawl_information_video(sub_key,main_key,link,tool,mode):
        tool.crawl_information_video(video_link=link, main_key=main_key, sub_key=sub_key,mode=mode)
        tool.driver.get('about:blank')
    
    @staticmethod
    def get_link_search_channel(queue_link,list_link_channels,tool,max_size_post):
        tool.get_link_search_channel(queue_link=queue_link,list_link_channels=list_link_channels,max_size_post=max_size_post)
        tool.driver.get('about:blank')



