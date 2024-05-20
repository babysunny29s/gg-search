import time
import queue
import threading
from read_config import *
from datetime import datetime, timedelta
from logger import logger
from SearchFacebook.scraper_post_search import ScraperPostSearch
from SearchFacebook.scraper_info_post import ScraperInfoPost
from SearchGoogle.search_gg import *
from SearchTiktok.crawl_post import CrawlPost
from SearchYoutube.get_link import Link
from SearchYoutube.search_youtube import DetailCrawler

def merge_list(list1, list2):
    for i in list2:
        if i in list1:
            continue
        else:
            list1.append(i)
    # merged_list = list1 + list2
    # unique_list = list(set(merged_list))
    return list1


def revert_time_range_to_period(start_time):
    time_range = calculate_time_period(start_time)
    if 0 < time_range <= 1:
        period = 'd'
    if 1 < time_range <= 7:
        period = 'w'
    if 7 < time_range <= 30:
        period = 'm'
    if 30 < time_range <= 365:
        period = 'y'
    return period


def check_created_time_in_range(start_time, created_time):
    current_time = int(time.time())  # Lấy timestamp của ngày hiện tại
    start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d')))  # Chuyển đổi ngày bắt đầu thành timestamp

    if start_time <= created_time <= current_time:
        return True
    else:
        return False
    
    
def worker_youtube(start_time, link_crawl_queue,data_post_queue):
    proxy = {
                        "http": "http://192.168.143.101:4016",
                        "https": "http://192.168.143.101:4016"
                }
    # proxy = {"http":"","https":""}
    
    while True:
        # Lấy công việc từ hàng đợi
        # data_post = []
        link = link_crawl_queue.get()
        tool = DetailCrawler()
        # tool.get_full_video_information(video_url=item,proxies=proxy)
        post = tool.get_full_video_information(video_url=link,proxies=proxy)
        if post:
            check_time = check_created_time_in_range(start_time, int(post.get('created_time')))
            if check_time:
                data_post_queue.put(post)
        # Xử lý công việc
        # ...

        # Đánh dấu công việc đã hoàn thành
        link_crawl_queue.task_done()


def queue_to_list(queue):
    my_list = list(queue.queue)
    return my_list


def write_list_to_file(file_path, my_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in my_list:
            file.write(str(item) + '\n')
    print("Danh sách đã được ghi vào file thành công.")
    

def filter_post(type:str, phrase:str, posts:list) -> list:
    '''Select post that contain 100% of phrases'''
    posts_filtered = []
    # Type : facebook, tiktok, youtube
    if type == "facebook":
        infor = ["content"]
    if type == "youtube":
        infor = ["title", "description"]
    if type == "tiktok":
        infor = ["title"]
    logger.info("Filter posts")
    for post in posts:
        for i in infor:
            content = post.get(i)
            content = content.lower()
            if phrase in content:
                posts_filtered.append(post)
                break
    del posts
    return posts_filtered


def search_and_getinfo_tiktok(phrase, start_time):
    try:
        logger.debug("Crawl tiktok")
        period = revert_time_range_to_period(start_time)
        links_gg = get_tiktok_result_by_ggsearch(phrase=phrase, period=period)
        se = CrawlPost(list_url=links_gg)
        data_post = se.etract_info_list_video()
        for post in data_post:
            check_time = check_created_time_in_range(start_time, int(post.get('created_time')))
            if check_time:
                continue
            else:
                data_post.remove(post)
        del se
        data_post = filter_post(type="tiktok", phrase=phrase, posts=data_post)
        return data_post
    except Exception as e:
        logger.error(e)
        return []


def search_and_getinfo_facebook(phrase, start_time):
    try:
        time_range = calculate_time_period(start_time)
        logger.debug("Crawl facebook")
        period = revert_time_range_to_period(start_time)
        current_day = datetime.now()
        datetime_start = datetime(current_day.year, current_day.month, current_day.day, current_day.hour, current_day.minute, current_day.second)
        time_line = datetime_start - timedelta(days=time_range)
        sc = ScraperPostSearch(time_line=time_line)
        data_post = sc.search_post(keyword=phrase)
        links_gg = get_facebook_result_by_ggsearch(phrase=phrase, period=period)
        for link in links_gg:
            if "facebook" not in link:
                links_gg.remove(link)
        scp = ScraperInfoPost()
        data_post_gg = scp.start_get_info(datasets=links_gg)
        for data in data_post_gg:
            data_post.append(data)
        data_post = filter_post(type="facebook", phrase=phrase, posts=data_post)
        write_list_to_file("link_fb.txt", data_post)
        return data_post
    except Exception as e:
        logger.error(e)
        return []
        
        
def search_and_getinfo_youtube(phrase, start_time):
    try:
        link_crawl_queue = queue.Queue()
        data_post_queue = queue.Queue()
        logger.debug("Crawl youtube")
        period = revert_time_range_to_period(start_time)
        data_post=[]
        gt = Link()
        links = gt.get_link_search(keyword=phrase,mode=period)
        links_gg = get_youtube_result_by_ggsearch(phrase=phrase, period=period)
        list_link = merge_list(links, links_gg)
        
        for link in list_link:
            if "watch" in link:
                link_crawl_queue.put(link)
                
        num_worker_threads = 10
        for i in range(num_worker_threads):
            t = threading.Thread(target=worker_youtube, args=(start_time, link_crawl_queue, data_post_queue))
            t.start()
        link_crawl_queue.join()
        data_post = queue_to_list(data_post_queue)
        data_post = filter_post(type="youtube", phrase=phrase, posts=data_post)
        return data_post
    except Exception as e:
        logger.error(e)
        return []


if __name__ == '__main__':
    search_and_getinfo_facebook(phrase = "nguyễn phú trọng", start_time="2024-04-22")

    

