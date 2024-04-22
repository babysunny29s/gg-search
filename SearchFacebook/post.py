class Post:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', '')
        self.id_encode = kwargs.get('id_encode', '')
        self.feedback_id = kwargs.get('feedback_id', '')
        self.feedback_expansion_token = kwargs.get('feedback_expansion_token', '')
        self.depth_comment = kwargs.get('depth_comment', 0)
        self.parent_id = kwargs.get('parent_id', '')
        self.type = kwargs.get('type', '')
        self.time_crawl = kwargs.get('time_crawl', '')
        self.link = kwargs.get('link', '')
        self.author_id = kwargs.get('author_id', '')
        self.author = kwargs.get('author', '')
        self.author_link = kwargs.get('author_link', '')
        self.avatar = kwargs.get('avatar', '')
        self.created_time = kwargs.get('created_time', '')
        self.content = kwargs.get('content', '')
        self.image_url = kwargs.get('image_url', [])
        self.like = kwargs.get('like', 0)
        self.comment = kwargs.get('comment', 0)
        self.haha = kwargs.get('haha', 0)
        self.wow = kwargs.get('wow', 0)
        self.sad = kwargs.get('sad', 0)
        self.love = kwargs.get('love', 0)
        self.angry = kwargs.get('angry', 0)
        self.care = kwargs.get('care', 0)
        self.share =  kwargs.get('share', 0)
        self.domain = kwargs.get('domain', 'facebook.com')
        self.hashtag =  kwargs.get('hashtag', [])
        #self.music = kwargs.get('music', '')
        #self.title = kwargs.get('title', '')
        #self.duration = kwargs.get('duration', 0 )
        #self.view = kwargs.get('view', 0)
        #self.description = kwargs.get('description', '')
        self.video = kwargs.get('video', [])
        self.source_id = kwargs.get('source_id', '')
        self.is_share = kwargs.get('is_share', 0)
        self.link_share = kwargs.get('link_share', '')
        self.type_share = kwargs.get('type_share', '')

    def is_valid(self) -> bool:
        is_valid = self.id != "" and self.author != "" and self.link != "" and self.created_time != "" 
        return is_valid

    def __str__(self) -> str:
        string = ""
        for attr_name, attr_value in self.__dict__.items():
            string =  f"{attr_name}={attr_value}\n" + string
        return string