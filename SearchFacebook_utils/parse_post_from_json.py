
import jsonpath_ng
from jsonpath_ng import parse, jsonpath
from SearchFacebook.post import Post
from datetime import datetime
import json
import base64
from datetime import datetime
import re
from urllib.parse import unquote
from SearchFacebook.utils import get_id_author_from_id_encode, write_log_json_post, get_id_post_from_id_encode
class ParserInfoPost:

    def __init__(self, post=None, path_file=""):
        self.path_file = path_file
        if post is None:    
            self.post = Post()
        else:
            self.post = post

    """
    Hàm này dùng để lấy thông tin về tác giả của bài đăng
    """
    def extract_post_author(self, jsondata, json_path= None, id_encode=""):
        try:
            post_author: str = ''
            post_author_id: str = ''
            post_author_link: str = ''
            post_author_avatar_link: str = ''
            if not id_encode:
                id_encode = jsondata['id']
                
            post_author_id = get_id_author_from_id_encode(id_encode)
            if not post_author_id:
                post_author_id = id_encode
            if json_path is None:
                json_path = parse("$.comet_sections.context_layout.story.comet_sections.actor_photo.story.actors")
            matches = json_path.find(jsondata)
            if matches:
                author_data = matches[0].value
                post_author_link = author_data[0]["url"]
                post_author = author_data[0]["name"]
                post_author_avatar_link = author_data[0]["profile_picture"]["uri"]
            if not post_author_link:
                post_author_link = "https://facebook.com/" + post_author_id


        except Exception as ex:
            print(f"extract_post_author {ex}")
        finally:
            return post_author, post_author_id, post_author_link, post_author_avatar_link

    """
    Hàm này dùng để lấy thông tin về thời gian của bài đăng
    """
    def extract_post_time(self, jsondata):
        try:
            post_time: str = ''
            json_path = parse("$.comet_sections.context_layout.story.comet_sections.metadata..story.creation_time")
            matches = json_path.find(jsondata)
            if matches:
                post_time = str(matches[0].value) #[0]['story']['creation_time']
            else:
                json_path2 = parse("$..comet_sections.metadata..story.creation_time")
                matches2 = json_path2.find(jsondata)
                if matches2:
                    post_time = str(matches2[0].value) #[0]['story']['creation_time']
        except Exception as ex:
            print(f"extract_post_time {ex}")
        finally:
            #print("End")
            return post_time

    """
    Hàm này dùng để lấy thông tin về content của bài đăng
    """
    def extract_post_content(self, jsondata):
        try:
            #print("Start")
            post_content_str: str = ''
            hashtag = []

            json_path = parse("$..content.story.comet_sections.message.story.message")
            matches = json_path.find(jsondata)
            
            if matches:
                content_data = matches[0].value
                post_content_str = content_data["text"]
                if "ranges" in content_data:
                    for entity_range in content_data["ranges"]:
                        if "entity" in entity_range:
                            url_hashtag = entity_range["entity"]["url"]
                            url_hashtag_decod = unquote(url_hashtag)
                            pattern = r'https://www.facebook.com/hashtag/([^/?]+)\?'
                            match = re.findall(pattern, url_hashtag_decod) 
                            for val in match:
                                hashtag_text = "#" + val
                                hashtag.append(hashtag_text)
                #print("End")  
            else: 
                json_path = parse("$..content..rich_message")
                matches = json_path.find(jsondata)
                if matches:
                    content_data = matches[0].value
                    for content in content_data:
                        text = content["text"]
                        post_content_str += text + " "
                        if "entity_ranges" in content:
                            for entity_range in content["entity_ranges"]:
                                if "entity" in entity_range:
                                    url_hashtag = entity_range["entity"]["url"]
                                    url_hashtag_decod = unquote(url_hashtag)
                                    pattern = r'https://www.facebook.com/hashtag/([^/?]+)\?'
                                    match = re.findall(pattern, url_hashtag_decod) 
                                    for val in match:
                                        hashtag_text = "#" + val
                                        hashtag.append(hashtag_text)
                    # post_content_str = content_data["text"]
                    #print("End")
                else:     
                    print("Post không có content")
            # json_path = parse("$..content..rich_message")
            # matches = json_path.find(jsondata)
            # if matches:
            #     content_data = matches[0].value
            #     for content in content_data:
            #         text = content["text"]
            #         post_content_str += text + " "
            #         if "entity_ranges" in content:
            #             for entity_range in content["entity_ranges"]:
            #                 if "entity" in entity_range:
            #                     url_hashtag = entity_range["entity"]["url"]
            #                     url_hashtag_decod = unquote(url_hashtag)
            #                     pattern = r'https://www.facebook.com/hashtag/([^/?]+)\?'
            #                     match = re.findall(pattern, url_hashtag_decod) 
            #                     for val in match:
            #                         hashtag_text = "#" + val
            #                         hashtag.append(hashtag_text)
            #     # post_content_str = content_data["text"]
            #     #print("End")
            # else:
            #     json_path = parse("$..content.story.comet_sections.message.story.message")
            #     matches = json_path.find(jsondata)
                
            #     if matches:
            #         content_data = matches[0].value
            #         post_content_str = content_data["text"]
            #         if "ranges" in content_data:
            #             for entity_range in content_data["ranges"]:
            #                 if "entity" in entity_range:
            #                     url_hashtag = entity_range["entity"]["url"]
            #                     url_hashtag_decod = unquote(url_hashtag)
            #                     pattern = r'https://www.facebook.com/hashtag/([^/?]+)\?'
            #                     match = re.findall(pattern, url_hashtag_decod) 
            #                     for val in match:
            #                         hashtag_text = "#" + val
            #                         hashtag.append(hashtag_text)
            #         #print("End")  
            #     else:          
            #         print("Post không có content")
        except Exception as ex:
            print(f"Cannot extract post content {ex}")
        return post_content_str, hashtag

    
    """
    Hàm này dùng để lấy thông tin link của bài đăng
    """
    def extract_post_link(self, jsondata):
        try:
            #print("Start")
            post_link: str = ""
            json_path = parse("$.comet_sections.context_layout.story.comet_sections.metadata..story.url")
            matches = json_path.find(jsondata)
            if matches:
                post_link = matches[0].value
            else:
                json_path = parse("$..comet_sections.metadata..story.url")
                matches = json_path.find(jsondata)
                if matches:
                    post_link = matches[0].value
                else:
                    print("Không lấy được link post")
        except Exception as ex:
            post_link = ""
            print(f"extract_post_link {ex}")
            # for item in metadata:
            #     if "story" in item and "url" in item["story"]:
            #         post_link = item["story"]["url"]
            #         break
            # #print("End")
        finally:
            #print("End")
            return post_link

    """
    Hàm này dùng để lấy thông tin id của bài đăng
    """
    def extract_post_id(self, jsondata):
        #print("Start")
        post_id = jsondata["post_id"]
        id_encode = jsondata["id"]
        #print("End")
        return post_id, id_encode

    """
    Hàm này dùng để lấy thông tin về media của bài đăng
    """
    def extract_post_media(self, jsondata, json_path_media=None):
        #print("Start")
        image_links = []
        video_links = []
        #trường hợp có 1 video và bị nhảy qua watch 


        #trường hợp có video và ảnh không quá 5 
        try:
            if json_path_media is None:
                json_path_media = parse("$.comet_sections.content.story.attachments")
            match_path_media = json_path_media.find(jsondata)
            if match_path_media:
                if not match_path_media[0].value:
                    print("Bài viết không có ảnh và video")
                    return image_links, video_links
                style_list = match_path_media[0].value[0]['style_list']
                if "album" in style_list:
                    list_media = list(match_path_media[0].value[0]['styles']['attachment']['all_subattachments']['nodes'])
                    media_count = int(match_path_media[0].value[0]['styles']['attachment']['all_subattachments']['count'])
                    if len(list_media) < media_count:
                        #trường hợp có ảnh và video >5
                        for media in list_media:
                            if media['media']['__typename'] == "Photo":
                                try:
                                    image_links.append(media['media']['viewer_image']['uri'])
                                except:
                                    image_links.append(media['media']['image']['uri'])
                            elif media['media']['__typename'] == "Video":
                                try:
                                    try:
                                        link_video = media['media']['video_grid_renderer']['video']['browser_native_hd_url']
                                    except:
                                        link_video = media['media']['video_grid_renderer']['video']['browser_native_sd_url']
                                    video_links.append(link_video)
                                    image_links.append(media['media']['viewer_image']['uri'])
                                except:
                                    image_links.append(media['media']['image']['uri'])
                    elif len(list_media) == media_count: #trường hợp ảnh + video < 5
                        for media in list_media:
                            if media['media']['__typename'] == "Photo":
                                try:
                                    image_links.append(media['media']['viewer_image']['uri'])
                                except:
                                    image_links.append(media['media']['image']['uri'])
                            elif media['media']['__typename'] == "Video":
                                try:
                                    try:
                                        link_video = media['media']['video_grid_renderer']['video']['browser_native_hd_url']
                                    except:
                                        link_video = media['media']['video_grid_renderer']['video']['browser_native_sd_url']
                                    video_links.append(link_video)
                                    image_links.append(media['media']['viewer_image']['uri'])
                                except:
                                    image_links.append(media['media']['image']['uri'])
                elif "photo" in style_list: #bài viết có 1 ảnh
                    media_ = match_path_media[0].value[0]['styles']['attachment']['media']
                    if media_['__typename'] == "Photo":
                        try:
                            image_links.append(media_['viewer_image']['uri'])
                        except:
                            image_links.append(media_['photo_image']['uri'])
                elif "video_inline" in style_list or "video" in style_list: #có 1 video nhưng không bị nhảy qua watch
                    media_ = match_path_media[0].value[0]['styles']['attachment']['media']
                    if media_['__typename'] == "Video":
                        try:
                            link_video = media_['browser_native_hd_url']
                            if link_video is None:
                                link_video = media_['browser_native_sd_url']
                        except:
                            link_video = media_['browser_native_sd_url']
                        video_links.append(link_video)
        except Exception as ex:
            print(f"Fail to extract photo and video in post {ex}")
        finally:
            #print("End")
            return image_links, video_links


    """
    Hàm này dùng để lấy thông tin về comments của bài đăng
    """
    def extract_post_comments(self, jsondata):
        try:
            list_id_comments = []
            display_coments = ParseCommentFromJson(file=self.path_file)
            display_coments._parser_comment(json_data=jsondata, list_id_comments=list_id_comments)
            print(f"Số comment trên giao diện là {len(list_id_comments)}")
            del display_coments
        except Exception as ex:
            print(f"Fail to extract display comment in post {ex}")
    
    """
    Hàm này dùng để lấy thông tin về reaction của bài đăng
    """
    def extract_post_reactions(self, jsondata):
        #print("Start")
        reactions = {
            "like" : 0,
            "haha" : 0,
            "wow" : 0,
            "sad" : 0,
            "love" : 0,
            "angry" : 0,
            "care" : 0
        } 
        id_reactions = {
            "1635855486666999" : "like",
            "115940658764963" : "haha",
            "478547315650144"  : "wow",
            "908563459236466"  : "sad",
            "1678524932434102"  : "love",
            "444813342392137"  : "angry",
            "613557422527858"  : "care"
        }
        try:
            json_path = parse("$..comet_ufi_summary_and_actions_renderer.feedback.top_reactions")
            matches = json_path.find(jsondata)
            if matches:
                reactions_data = matches[0].value
                for item in reactions_data["edges"]:
                    # reaction_name = item["node"]["localized_name"].lower()
                    # reaction_count = item["reaction_count"]
                    # reactions[reaction_name] = reaction_count
                    if item["node"]["id"] in id_reactions:
                        reaction_count = item["reaction_count"]
                        reactions[id_reactions[item["node"]["id"]]] = reaction_count
                #print("End")
            else: 
                print("cannot extract post reactions")
        except Exception as ex:
            print(ex)
        finally:
            return reactions

    """
    Hàm này dùng để lấy thông tin về số comment của bài đăng
    """
    def extract_total_comment(self, jsondata):
        #print("Start")
        total_comment = 0
        try:
            json_path2 = parse("$..comet_ufi_summary_and_actions_renderer.feedback")
            matches2 = json_path2.find(jsondata)
            if matches2:
                comment_data = matches2[0].value
                try:
                    total_comment = comment_data["total_comment_count"]
                except:
                    try:
                        total_comment = comment_data['comments_count_summary_renderer']['feedback']['comment_rendering_instance']['comments']['total_count']
                    except:
                        total_comment = comment_data['comment_rendering_instance']['comments']['total_count']
            else:
                print("cannot extract post comment_count")
        except Exception as e:
            print(e)
        finally:
            #print("End")
            return total_comment
    
    """
    Hàm này dùng để lấy thông tin về số lượt share của bài đăng
    """
    def extract_post_share(self, jsondata):
        #print("Start")
        share = 0
        json_path = parse("$..share_count")
        matches = json_path.find(jsondata)
        if matches:
            share_data = matches[0].value
            share = share_data["count"]
            #print("End")
        else:
            print("cannot extract post share_count")
        return share

    """
    Hàm này dùng để lấy thông tin về các link share, bài share của bài đăng
    """
    def extract_post_share_link(self, jsondata):
        try:
            is_share = 0
            link_share = ""
            type_share = ""
            #print("Start")
            json_path_share_story = parse("$..attached_story.comet_sections.context_layout.story.comet_sections.metadata")
            json_path_share_link = parse("$.comet_sections.content.story.attachments")
            match_story_share = json_path_share_story.find(jsondata)
            match_link_share = json_path_share_link.find(jsondata)
            #trường hợp share bài post facebook
            if match_story_share:
                #lấy link bài share
                link_share = match_story_share[0].value[0]['story']['url'] 
                if link_share != "":
                    is_share = 1
                    type_share = "post"
                    
                    #lấy thông tin  bài share
                    post = Post(link=link_share)
                    if "group" in link_share.lower():
                        post.type = "facebook group"
                    else:
                        post.type = "facebook page"
                    #lấy thông tin id bài share
                    # tracking_path = parse("$..feedback.story.tracking")
                    # match_tracking = tracking_path.find(jsondata)
                    # if match_tracking:
                    try:
                        # json_tracking = json.loads(match_tracking[0].value)
                        # id_post_share = json_tracking['original_content_id']
                        #post.id = id_post_share
                        post.time_crawl = str(int(datetime.timestamp(datetime.now())))
                        post.created_time = match_story_share[0].value[0]['story']['creation_time']
                        #lấy thông tin tác giả của bài share
                        path_author = parse("$..attached_story.comet_sections.context_layout.story.comet_sections.actor_photo.story.actors")
                        path_id_encode_post_share = parse("$..attached_story.comet_sections.context_layout.story.comet_sections.actor_photo.story.id")
                        match_id_encode_post_share = path_id_encode_post_share.find(jsondata)
                        if match_id_encode_post_share:
                            id_encode_post_share = match_id_encode_post_share[0].value
                            post.id = get_id_post_from_id_encode(id_encode_post_share)
                            post.id_encode = id_encode_post_share
                            post.author, post.author_id, post.author_link, post.avatar = self.extract_post_author(jsondata=jsondata, json_path=path_author, id_encode=id_encode_post_share)
                            #lấy thông tin content của bài viết
                            try:
                                content_path = parse("$..comet_sections.content.story.attached_story.comet_sections.message.story.message")
                                match_content = content_path.find(jsondata)
                                if match_content:
                                    post.content = match_content[0].value['text']
                                else:
                                    content_path = parse("$..comet_sections.content.story.attached_story.message")
                                    match_content = content_path.find(jsondata)
                                    if match_content:
                                        post.content = match_content[0].value['text']
                                    else:
                                        content_path = parse("$..comet_sections.content.story.comet_sections.attached_story.story.attached_story.comet_sections.attached_story_layout.story.comet_sections.message.story.message")
                                        match_content = content_path.find(jsondata)
                                        if match_content:
                                            post.content = match_content[0].value['text']
                                        else:
                                            print("Không tìm thấy content post share")

                            except Exception as e:
                                print(f"Cannot extract content post share {e}")
                            
                            #lấy thông tin media bài share
                            json_path_media = parse("$.comet_sections.content.story.attached_story.attachments")
                            post.image_url, post.video =  self.extract_post_media(jsondata=jsondata, json_path_media=json_path_media)

                            #lấy thông tin type của post
                            write_log_json_post(post=post, file=self.path_file)
                            print(f"Đẩy post {post.id} qua kafka")
                        else:
                            print("Không lấy được id của post share")
                        
                        #push_kafka(posts=[post])

                    except Exception as ex:
                        print(f"Error {ex}")
                    # else:
                    #     print("Không tìm được id bài share")
                    del post




            #trường hợp share link
            elif match_link_share:
                style_list = match_link_share[0].value[0]['style_list']
                if "share" in style_list:
                    link_share = match_link_share[0].value[0]['styles']['attachment']['story_attachment_link_renderer']['attachment']['web_link']['url']
                    if link_share != "":
                        is_share = 1
                        type_share = "link"
            
        except Exception as ex:
            print(ex)
        finally:
            #print("End")
            return is_share, link_share, type_share
    def extract(self, jsondata):

        self.post.author, self.post.author_id, self.post.author_link, self.post.avatar = self.extract_post_author(jsondata)
        self.post.created_time = self.extract_post_time(jsondata)

        self.post.content, self.post.hashtag =  self.extract_post_content(jsondata)

        #if self.post.id == "":
        self.post.id, self.post.id_encode = self.extract_post_id(jsondata)

        if self.post.link == "":
            link = self.extract_post_link(jsondata)
            if link == "":
                if self.post.id == "":
                    print("Post không có id")
                else:
                    link = "https://www.facebook.com/" + str(self.post.id)
            self.post.link = link
        if not self.post.type:
            if "group" in self.post.link.lower():
                self.post.type = "facebook group"
            else:
                self.post.type = "facebook page"
        reactions = self.extract_post_reactions(jsondata)
        self.post.comment  = self.extract_total_comment(jsondata)
        self.post.share = self.extract_post_share(jsondata)
        self.post.is_share, self.post.link_share, self.post.type_share = self.extract_post_share_link(jsondata)
        self.post.image_url, self.post.video = self.extract_post_media(jsondata) 

        self.post.time_crawl = str(int(datetime.timestamp(datetime.now())))
        
        self.post.like, self.post.haha, self.post.wow, self.post.sad, self.post.love, self.post.angry, self.post.care = reactions['like'], reactions['haha'], reactions['wow'], reactions['sad'], reactions['love'], reactions['angry'], reactions['care']
       
        write_log_json_post(post=self.post, file=self.path_file)
        if self.post.is_valid():
            print(f"Đẩy post {self.post.id} qua kafka")
            #push_kafka(posts=[self.post])
            del self.post
            self.extract_post_comments(jsondata)

class ParseCommentFromJson:
    
    def __init__(self, file="") -> None:
        self.data_comment = None
        self.list_comment = []
        self.list_post_comments = []
        self.file = file

    def _write_log_error(self, data : str,  file = ""):
        if file == "":
            file = "logError.txt"
        with open(file, "a", encoding="utf-8") as fp:
            fp.write(data)
            fp.write("\n")
    # def _get_data_json(self, json_data):
    #     path_type_1 = parse("$..node.comment_rendering_instance_for_feed_location.comments")
    #     path_type_2 = parse("$..node.replies_connection")
    #     match_1 = path_type_1.find(json_data)
    #     match_2 = path_type_2.find(json_data)
    #     if match_1:
    #         self.list_comment = match_1[0].value['edges']
    #     elif match_2:
    #         self.list_comment = match_2[0].value['edges']
    #     else:
    #         print("Cannot find comments")
    def _get_data_json(self, json_data):
        try:
            #print("Start")
            print("Get comments from json data")
            path_type_1 = parse("$..comet_sections.feedback.story.feedback_context.interesting_top_level_comments")
            path_type_2 = parse("$..replies_connection.edges")

            match_1 = path_type_1.find(json_data)
            match_2 = path_type_2.find(json_data)
            print(len(match_2))
            if not match_1 and not match_2:
                print("Json old version facebook")
                path_type_3 = parse("$..display_comments.edges")
                match_3 = path_type_3.find(json_data)
                print(len(match_3))
                if match_3:
                    for match in match_3:
                        self.list_comment.extend(match.value)
            else:
                if match_1:
                    for match in match_1:
                        self.list_comment.extend(match.value)
                if match_2:
                    for match in match_2:
                        self.list_comment.extend(match.value)

            if len(self.list_comment) == 0:
                print("Cannot find comments in json data")
            #print("End")
        except Exception as ex:
            print(f"Error load comments from json {ex}")
            self._write_log_error(f"Error load comments from json {ex}")
            self._write_log_error(json.dumps(json_data))

    def __ex_author(self, comment_info, comment_post: Post):
        try:
            #print("Start")
            comment_post.author = comment_info['comment']['author']['name']
            comment_post.author_link = comment_info['comment']['author']['url']
            try:
                comment_post.avatar = comment_info['comment']['user']['profile_picture']['uri']
            except:
                comment_post.avatar = comment_info['comment']['author']['profile_picture_depth_0']['uri']
            #print("End")
        except Exception as ex:
            print(f"Cannot extract author info {ex}")
            self._write_log_error(f"Cannot extract author info {ex}")
            #self._write_log_error(json.dumps(comment_info))
    def __ex_reactions(self, comment_info, comment_post: Post):
        try:
            #print("Start")
            reactions = {
                "1635855486666999" : "like",
                "1678524932434102" : "love",
                "478547315650144"  : "wow",
                "613557422527858"  : "care",
                "115940658764963"  : "haha",
                "908563459236466"  : "sad",
                "444813342392137"  : "angry",
            }
            top_reactions = comment_info['comment']['feedback']['top_reactions']['edges']
            for react in top_reactions:
                try:
                    comment_post.__dict__[reactions[react['node']['id']]] = react['reaction_count']
                except:
                    print(f"Error reaction {react['node']['id']}")
            #print("End")
        except Exception as ex:
            print(f"Cannot extract reactions comment {ex}")
            self._write_log_error(f"Cannot extract reactions comment {ex}")
            #self._write_log_error(json.dumps(comment_info))
    def __ex_media(self, comment_info, comment_post: Post):
        try:
            #print("Start")
            images = []
            videos = []
            list_media = comment_info['comment']['attachments']
            if not list_media:
                print("Comment not image and video")
                comment_post.image_url = images
                comment_post.video = videos
            else:
                for media in list_media:
                    try:
                        if 'photo' in media['style_list']:
                            images.append(media['style_type_renderer']['attachment']['media']['image']['uri'])
                        elif 'animated_image_share' in media['style_list']:
                            try:
                                images.append(media['style_type_renderer']['attachment']['animated_image']['uri'])
                            except:
                                try:
                                    images.append(media['style_type_renderer']['attachment']['media']['animated_image']['uri'])
                                except:
                                    images.append(media['style_type_renderer']['attachment']['media']['image']['uri'])
                        elif 'video_inline' in media['style_list']:
                            try:
                                videos.append(media['style_type_renderer']['attachment']['media']['browser_native_hd_url'])
                            except:
                                videos.append(media['style_type_renderer']['attachment']['media']['browser_native_sd_url'])
                        elif 'sticker' in media['style_list']:
                            images.append(media['style_type_renderer']['attachment']['media']['image']['uri'])
                    except Exception as e:
                        print(f"Cannot get link media from {media} {e}")
                comment_post.image_url = images
                comment_post.video = videos
            #print("End")            
        except Exception as ex:
            print(f"Cannot extract media comment {ex}")
            self._write_log_error(f"Cannot extract media comment {ex}")
            #self._write_log_error(json.dumps(comment_info))
    def __ex_info_share(self, comment_info, comment_post: Post):
        pass
    def __ex_info_comment(self, comment_info, comment_post: Post):
        try:
            #print("Start")
            comment_post.type = "facebook comment"
            comment_post.time_crawl = str(int(datetime.timestamp(datetime.now())))
            comment_post.created_time = str(comment_info['comment']['created_time'])
            comment_post.domain = "facebook.com"
            comment_post.source_id = comment_info['comment']['parent_feedback']['share_fbid']
            #print("End")
        except Exception as ex:
            print(f"Cannot extract comment info {ex}")
            self._write_log_error(f"Cannot extract comment info {ex}")
            #self._write_log_error(json.dumps(comment_info))

    def __ex_content_comment(self, comment_info, comment_post: Post):
        try:
            #print("Start")
            if comment_info['comment']['body_renderer'] is None and comment_info['comment']['body'] is None:
                print("Comment has no content")
                comment_post.content = ""
                return
            try:
                comment_post.content = comment_info['comment']['body_renderer']['text']
            except:
                print("Retry extract content")
                comment_post.content = comment_info['comment']['body']['text']
            #print("End")
        except Exception as ex:
            print(f"Cannot extract content comment {ex}")
            self._write_log_error(f"Cannot extract content comment {ex}")
            #self._write_log_error(json.dumps(comment_info))

    def __ex_id_comment(self, comment_info, comment_post: Post):
        try:
            #print("Start")
            depth = int(comment_info['comment']['depth'])
            if depth == 0: #comment cấp 1 id là id comment
                comment_post.id = comment_info['comment']['legacy_fbid']
            elif depth == 1: # reply comment id là id_rely.id_comment
                id_rely = comment_info['comment']['legacy_fbid']
                id_comment_base64 = comment_info['comment']['comment_parent']['id']
                try:
                    id_comment_decode = base64.b64decode(id_comment_base64).decode("utf-8")
                    id_comment_parent = id_comment_decode.split('_')[-1]
                    comment_post.id = id_comment_parent + "." + id_rely
                except:
                    comment_post.id = comment_info['comment']['legacy_fbid']
            elif depth == 2: #reply của reply comment
                id_rely = comment_info['comment']['legacy_fbid']
                id_comment_base64 = comment_info['comment']['comment_parent']['id']
                try:
                    id_comment_decode = base64.b64decode(id_comment_base64).decode("utf-8")
                    id_comment_parent = id_comment_decode.split('_')[-1]
                    comment_post.id = id_comment_parent + "." + id_rely
                except:
                    comment_post.id = comment_info['comment']['legacy_fbid']

            comment_post.link = "https://www.facebook.com/" + comment_info['comment']['legacy_fbid']
            #print("End")
        except Exception as ex:
            print(f"Cannot extract comment id {ex}")
            self._write_log_error(f"Cannot extract comment id {ex}")
            #self._write_log_error(json.dumps(comment_info))

    def __ex_interact_comment(self, comment_info, comment_post: Post):
        try:
            #print("Start")
            depth = int(comment_info['comment']['depth'])
            if depth == 0: #comment cấp 1
                try:
                    comment_post.comment = comment_info['comment']['feedback']['total_comment_count']
                except Exception as e:
                    comment_post.comment = comment_info['comment']['feedback']['replies_fields']['total_count']
            elif depth == 1: # reply comment
                try:
                    comment_post.comment = comment_info['comment']['feedback']['total_comment_count']
                except Exception as e:
                    comment_post.comment = comment_info['comment']['feedback']['replies_fields']['total_count']
            elif depth == 2: #reply của reply comment
                comment_post.comment = 0
            #print("End")
        except Exception as ex:
            print(f"Cannot extract interact comment {ex}")
    def _parser_comment(self, json_data, list_id_comments):
        #print("Start")
        ## Lấy số comment được render bằng json phiên bản mới
        self._get_data_json(json_data)
        print(f"số comment là {len(self.list_comment)}")

        for comment_info in self.list_comment:
            comment_post = Post()
            try:
                self.__ex_id_comment(comment_info, comment_post)
                if comment_post.id == '':
                    continue
                if comment_post.id in list_id_comments:
                    continue
                else:
                    list_id_comments.append(comment_post.id)
                
                #extract infomation author comment
                self.__ex_author(comment_info, comment_post)
                self.__ex_info_comment(comment_info, comment_post)
                self.__ex_content_comment(comment_info, comment_post)

                self.__ex_reactions(comment_info, comment_post)
                self.__ex_interact_comment(comment_info, comment_post)
                self.__ex_media(comment_info, comment_post)
                
                if comment_post.is_valid():

                    write_log_json_post(post=comment_post, file=self.file)
                    self.list_post_comments.append(comment_post)
                else:
                    print("Comment is not valid")
                    self._write_log_error("Comment is not valid")
                    self._write_log_error(json.dumps(comment_post))
            except Exception as ex:
                print(f"Error parse comment {ex}")
            del comment_post
        print(f"Số bài comments đẩy qua kafka là {len(self.list_post_comments)}")

        #push_kafka(posts=self.list_post_comments)
        #print("End")

