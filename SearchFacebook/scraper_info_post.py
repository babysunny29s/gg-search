import requests
from SearchFacebook.define_api import *
from SearchFacebook.get_id_post_from_link import get_id_post
from SearchFacebook.api_get_post import get_infor_posts_page_from_api, get_infor_post_group
import json
from SearchFacebook.parse_post_from_json import ParserInfoPost
from jsonpath_ng import parse
from SearchFacebook.post import Post
from datetime import datetime
from requests_html import HTMLSession
from SearchFacebook.utils import get_id_author_from_id_encode, encode_base64
from SearchFacebook.api_get_storyID_from_photo import get_storyID_from_id_photo

class ScraperInfoPost:
    def __init__(self) -> None:
        self.SESSION = None
        self.HTMLSESSION = None
        self.bCheck = True
        self.__create_session()
    def __create_session(self):
        print(f">> Create session")
        self.SESSION = requests.Session()
        self.HTMLSESSION = HTMLSession()
        #self.proxy_use = rotate_proxy(self.PROXY, self.proxy_use)
        self.SESSION.headers.update(HEADERS)
        self.HTMLSESSION.headers.update(HEADERS)
        #self.SESSION.proxies.update(self.proxy_use)
    def __process_data_infor(self, data, group_id=None, page_id=None, path_file=""):
        matches = data.split("\n")
        print(f">> số json trả về là {len(matches)}")
        data_post =[]
        for i, match in enumerate(matches):
            try:
                json_match = json.loads(match)
                #if i == 0:
                path_id = parse("$.data.node")
                match_id = path_id.find(json_match)
                if match_id:
                    node_post = match_id[0].value
                    if node_post['__typename'] == "Story":
                        post_id = node_post['post_id']
                        #lấy thông tin cơ bản của bài viết
                        if group_id:
                            post = Post(id=post_id, parent_id=group_id, type="facebook group")
                        elif page_id:
                            post = Post(id=post_id,  type="facebook page")
                        info_post = ParserInfoPost(post=post, path_file=path_file)
                        info_post.extract(jsondata=node_post)                          
                        del info_post
                        data_post.append(post.__dict__)
                        del post                        
                    else:
                        print(f">> Node không phải là Story")
                else:
                    print(f">> Không tìm thấy Node")
            except Exception as ex:
                print(f">> Error func __processing_data: {ex}")
        return data_post
    def __scaper_post(self, url, path_file):
        try:
            data_post = None
            type_link, id_, group_id = get_id_post(url=url, session=self.HTMLSESSION)
            if type_link == "story":
                if id_:
                    if group_id:
                        response = get_infor_post_group(groupID=group_id, session=self.SESSION, storyID=id_)
                        if not response:
                            print(f"Không lấy được thông tin post {url}")
                        data_post = self.__process_data_infor(data=response, group_id=group_id, path_file=path_file)
                    else:
                        response = get_infor_posts_page_from_api(session=self.SESSION, storyID=id_)
                        if not response:
                            print(f"Không lấy được thông tin post {url}")
                        page_id = get_id_author_from_id_encode(id_)
                        data_post = self.__process_data_infor(data=response, page_id=page_id, path_file=path_file)
            elif type_link == "photo":
                storyID = get_storyID_from_id_photo(session=self.SESSION, id_photo=id_)
                if storyID:
                    response = get_infor_posts_page_from_api(session=self.SESSION, storyID=storyID)
                    if not response:
                        print(f"Không lấy được thông tin post {url}")
                    page_id = get_id_author_from_id_encode(storyID)
                    data_post = self.__process_data_infor(data=response, page_id=page_id, path_file=path_file)
            elif type_link == "video":
                sID = f"S:_I{group_id}:VK:{id_}"
                storyID = encode_base64(input_string=sID)
                response = get_infor_posts_page_from_api(session=self.SESSION, storyID=storyID)
                if not response:
                    print(f"Không lấy được thông tin post {url}")
                data_post = self.__process_data_infor(data=response, page_id=group_id, path_file=path_file)
            else:
                # data_post = None
                print(f"Error link {url}")
            return data_post
        except Exception as e:
            print(f"Error fun __scaper_post {e}")
        
                
    def start_get_info(self, datasets: list):
        print(f"Số link có trong datasets là {len(datasets)}")
        name_file = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        path_file = f"db/Search/{name_file}.json"
        data_posts = []
        for i, url in enumerate(datasets):
            print(f"Scraper {url} >>>> {i+1}")
            data_post = self.__scaper_post(url, path_file)
            if data_post:
                data_posts.extend(data_post)
        return data_posts