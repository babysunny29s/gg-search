
from api_search import get_data_post_search
import requests
from define_api import *
import json
from jsonpath_ng import parse
from post import Post
from parse_post_from_json import ParserInfoPost
from utils import check_time_line_expired
class ScraperPostSearch:
    def __init__(self, time_line, MAX_SIZE_POST=50) -> None:
        self.SESSION = None
        self.time_line = time_line
        self.MAX_SIZE_POST = MAX_SIZE_POST
        self.idem = 0
        self.bCheck = True
        self.check_time_expired = False
        self.__create_session()
    def __create_session(self):
        print(f">> Create session")
        self.SESSION = requests.Session()
        #self.proxy_use = rotate_proxy(self.PROXY, self.proxy_use)
        self.SESSION.headers.update(HEADERS)
        #self.SESSION.proxies.update(self.proxy_use)
    def __reset_params(self):
        self.idem = 0
        self.bCheck = True
        self.check_time_expired = False
    def __parse_end_cursor(self, json_data):
        try:
            cursor = json_data['data']['serpResponse']['results']['page_info']['end_cursor']
            return cursor
        except Exception as e:
            print(f">> Error func parse_end_cursor: {e}")
            return ""
    
    def __processing_data(self, data, keyword: str):
        cursor = ""
        matches = data.split("\n")
        print(f">> Số json trả về là {len(matches)}")
        for i, match in enumerate(matches):
            try:
                json_match = json.loads(match)
                if i == 0:
                    path_id = parse("$.data.serpResponse.results.edges")
                    match_id = path_id.find(json_match)
                    if match_id:
                        list_node_post = match_id[0].value
                        cursor = self.__parse_end_cursor(json_match)
                        for node_post_search in list_node_post:
                            node_story = node_post_search['relay_rendering_strategy']['view_model']['click_model']['story']
                            post_id = node_story['post_id']
                            #lấy thông tin cơ bản của bài viết
                            post = Post(id=post_id)
                            
                            info_post = ParserInfoPost(post=post, path_file=f"db/Search/{keyword.replace(' ', '_')}_info.json")
                            info_post.extract(jsondata=node_story)
                            self.idem += 1
                            create_time_post = post.created_time
                            del info_post
                            del post
                            print(f">> Time create post {post_id} {create_time_post}")
                            if self.time_line is not None:
                                if check_time_line_expired(create_time_post, self.time_line):
                                    print(f">> Thời gian bài đăng đã quá {self.time_line}")
                                    self.check_time_expired =  True
                                    return cursor
            except Exception as ex:
                print(f">> Error func __processing_data: {ex}")
        return cursor
    def __check_done(self):
        if self.check_time_expired:
            if self.time_line:
                print(f">> Tất cả bài viết trong group, page đã quá thời gian {self.time_line}")
                self.bCheck = False
        if self.idem > self.MAX_SIZE_POST and self.MAX_SIZE_POST != -1:
            print(f">> Đã lấy đủ số lượng bài ưu cầu")
            self.bCheck = False
    def __scraper_post_search(self, keyword: str):
        try:
            self.__reset_params()
            results = get_data_post_search(session=self.SESSION, text=keyword)
            if results is None:
                print("Không có data trả về từ server")
                return
            end_cursor = self.__processing_data(data=results, keyword=keyword)
            self.__check_done()
            while self.bCheck:
                if end_cursor:
                    results = get_data_post_search(session=self.SESSION, text=keyword, cursor=end_cursor)
                    end_cursor = self.__processing_data(data=results, keyword=keyword)
                    self.__check_done()
                else:
                    self.bCheck = False
                    break
            print(f">> Scraper done key {keyword}, number post {self.idem}")
        except Exception as e:
            print(f">> Error func scaper_group: {e}")
    def search_post(self, keyword: str):
        print(f"Search các bài viết trên facebook với từ khóa {keyword}")
        self.__scraper_post_search(keyword=keyword)

