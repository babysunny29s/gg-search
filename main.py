import time
import ast
from datetime import datetime, timedelta
from logger import logger
from read_config import read_config
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


def revert_time_range_to_period(time_range):
    if 0 < time_range <= 1:
        period = 'd'
    if 1 < time_range <= 7:
        period = 'w'
    if 7 < time_range <= 30:
        period = 'm'
    if 30 < time_range <= 365:
        period = 'y'
    return period

def check_created_time_in_range(created_time):
    current_time = int(time.time())  # Lấy timestamp của ngày hiện tại
    start_time = int(time.mktime(time.strptime('2024-04-17', '%Y-%m-%d')))  # Chuyển đổi ngày bắt đầu thành timestamp

    if start_time <= created_time <= current_time:
        return True
    else:
        return False
        

def search_and_getinfo_youtube(phrase, time_range):
    period = revert_time_range_to_period(time_range)
    data_post=[]
    gt = Link()
    links = gt.get_link_search(keyword=phrase,mode=period)
    links_gg = get_youtube_result_by_ggsearch(phrase=phrase, period=period)
    list_link = merge_list(links, links_gg)
    proxy = {
                        "http": "http://192.168.143.101:4016",
                        "https": "http://192.168.143.101:4016"
                }
    for link in list_link:
        if "watch" in link:
            tool = DetailCrawler()
            post = tool.get_full_video_information(video_url=link,proxies=proxy)
            if post:
                check_time = check_created_time_in_range(int(post.get('created_time')))
                if check_time:
                    data_post.append(post)
    data_post = filter_post(type="youtube", phrase=phrase, posts=data_post)
    return data_post


def search_and_getinfo_facebook(phrase, time_range):
    period = revert_time_range_to_period(time_range)
    current_day = datetime.now()
    datetime_start = datetime(current_day.year, current_day.month, current_day.day, current_day.hour, current_day.minute, current_day.second)
    time_line = datetime_start - timedelta(days=time_range)
    sc = ScraperPostSearch(time_line=time_line)
    data_post = sc.search_post(keyword=phrase)
    # links_gg = get_facebook_result_by_ggsearch(phrase=phrase, period=period)
    # for link in links_gg:
    #     if "facebook" not in link:
    #         links_gg.remove(link)
    # scp = ScraperInfoPost()
    # data_post_gg = scp.start_get_info(datasets=links_gg)
    data_post = filter_post(type="facebook", phrase=phrase, posts=data_post)
    return data_post
    
    
def search_and_getinfo_tiktok(phrase, time_range):
    period = revert_time_range_to_period(time_range)
    links_gg = get_tiktok_result_by_ggsearch(phrase=phrase, period=period)
    se = CrawlPost(list_url=links_gg)
    data_post = se.etract_info_list_video()
    del se
    data_post = filter_post(type="tiktok", phrase=phrase, posts=data_post)
    return data_post


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
    

def main():
    phrase, time_range = read_config()
    # GET YOUTUBE
    
    data_post_tiktok = search_and_getinfo_tiktok(phrase, time_range)
    data_post_facebook = search_and_getinfo_facebook(phrase, time_range)
    data_post_youtube = search_and_getinfo_youtube(phrase, time_range)
    all_data_post = data_post_facebook + data_post_tiktok + data_post_youtube
    with open("output.txt", 'a', encoding='utf-8') as f:
        for item in all_data_post:
        # data2 = ast.literal_eval(str(data)) 
            print("❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️")
            f.write(f'{item}\n')
    
    
main()