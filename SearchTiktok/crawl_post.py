import os
import pickle
import requests

import json
import time

from bs4 import BeautifulSoup
# from kafka import KafkaProducer
from SearchTiktok.post_tiktok_etractor import PostTikTokExtractor, PostCommentExtractor, PostReplyExtractor
from logger import logger
from urllib.parse import urlencode as encoder

  
class CrawlPost:
    def __init__(self,list_url) -> None:
        self.list_url = list_url

    def get_info_video(self, url , video_id):
        # logger.debug(f"Start crawl link {url}")
        try:
            proxies = {
                'http': 'http://172.168.201.2:4010',
                'https': 'http://172.168.201.2:4010'
            }
            posts = []
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "authority": "www.tiktok.com",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Host": "www.tiktok.com",
                "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
            }
            # res = requests.get(url=self.url, headers=headers, proxies=proxies)
            res = requests.get(url=url, headers=headers)
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__')
            json_data = script_tag.string.strip()
            json_data = json.loads(json_data)
            infor_text = json_data["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
            post_extractor: PostTikTokExtractor = PostTikTokExtractor(link=url,source_id=video_id ,infor_text=infor_text)
            post = post_extractor.extract()
            del post_extractor
            if post is not None:
                return post.__dict__
            else: 
                return None
        except Exception as e:
            logger.warning(e)
            
    def etract_info_list_video(self):
        data_post = []
        # list_url = self.list_url
        for url in self.list_url:
            video_id = url.split("/")[5].split("?", 1)[0]
            post = self.get_info_video(url, video_id)
            if post:
                data_post.append(post)
        return data_post
                
    
 