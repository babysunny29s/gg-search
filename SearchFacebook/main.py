# from api_search import get_data_post_search
# import requests
# from define_api import *
from scraper_post_search import ScraperPostSearch
import os
from datetime import datetime, timedelta
from scraper_info_post import ScraperInfoPost
# ss = requests.session()
# ss.headers.update(HEADERS)
# results = get_data_post_search(session=ss, text="nguyễn văn chiến")
# print(results)


# with open("response.txt", "w", encoding="utf-8") as fp:
#     fp.write(results)
if not os.path.exists("db/Search"):
    os.makedirs("db/Search")

def main_search_post_fb():
    print(
        
    "\n                    _oo0oo_                      \n"
    "                   o8888888o                       \n"
    "                   88' . '88                       \n"
    "                   (| -_- |)                       \n"
    "                   0\  =  /0                       \n"
    "                 ___/`---'\___                     \n"
    "               .' \\|     |// '.                   \n"
    "              / \\|||  :  |||// \                  \n"
    "             / _||||| -:- |||||- \                 \n"
    "            |   | \\\  -  /// |   |                \n"
    "            | \_|  ''\---/''  |_/ |                \n"
    "             \ .-\__  '-' ___/-. /                 \n"
    "           ___'. .' /--.--\ `. .'___               \n"
    "        ."" '< `.___\_<|>_/___.' >' "".            \n"
    "      | | :  `- \`.;`\ _ /`;.`/ - ` : | |          \n"
    "      \  \ `_.   \_ __\ /__ _/   .-` /  /          \n"
    "  =====`-.____`.___ \_____/___.-`___.-'=====       \n"
    "                    `=---='                        \n"
    "            It works … on my machine               \n"
    "  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      \n"
 
    )
    number_day_post = 1  #Thời gian lấy bài trong search, đơn vị ngày
    Max_post = 50   # Số post tối đa
    keyword = "Nguyễn Phú Trọng đốt lò" #Từ khóa search
    current_day = datetime.now()
    datetime_start = datetime(current_day.year, current_day.month, current_day.day, current_day.hour, current_day.minute, current_day.second)
    time_line = datetime_start - timedelta(days=number_day_post)
    print(f"==============TimeLine : {time_line}=================")
    sc = ScraperPostSearch(time_line=time_line, MAX_SIZE_POST=Max_post)
    sc.search_post(keyword=keyword)

def main_get_post_from_link():
    print(
        
    "\n                    _oo0oo_                      \n"
    "                   o8888888o                       \n"
    "                   88' . '88                       \n"
    "                   (| -_- |)                       \n"
    "                   0\  =  /0                       \n"
    "                 ___/`---'\___                     \n"
    "               .' \\|     |// '.                   \n"
    "              / \\|||  :  |||// \                  \n"
    "             / _||||| -:- |||||- \                 \n"
    "            |   | \\\  -  /// |   |                \n"
    "            | \_|  ''\---/''  |_/ |                \n"
    "             \ .-\__  '-' ___/-. /                 \n"
    "           ___'. .' /--.--\ `. .'___               \n"
    "        ."" '< `.___\_<|>_/___.' >' "".            \n"
    "      | | :  `- \`.;`\ _ /`;.`/ - ` : | |          \n"
    "      \  \ `_.   \_ __\ /__ _/   .-` /  /          \n"
    "  =====`-.____`.___ \_____/___.-`___.-'=====       \n"
    "                    `=---='                        \n"
    "            It works … on my machine               \n"
    "  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      \n"
 
    )
    #Truyền vào 1 list danh sách các link cần lấy
    list_link = [
        # "https://www.facebook.com/photo.php?fbid=1312422689587429&set=a.1164193941076972&type=3&paipv=0&eav=AfbRQlAA4D6dW0qKP_Ybrfuy3bgaBS2vOpUAMU3GiJ2NPc1251xcWn-Y4yeU0BLhSf8&_rdr",
        # "https://www.facebook.com/nguyenhoan2711/posts/pfbid0zev9rEj9seWBdtGhrvqU42t3zt7SxrPPWu3XZgAdS8vVaavbiTcotyug4JRbLZVnl",
        # "https://www.facebook.com/groups/315078553070255/posts/1115235386387897/",
        "https://www.facebook.com/thongtinchinhphu/posts/-t%E1%BB%95ng-b%C3%AD-th%C6%B0-nguy%E1%BB%85n-ph%C3%BA-tr%E1%BB%8Dng-g%E1%BB%ADi-th%C6%B0-ch%C3%BAc-m%E1%BB%ABng-n%C4%83m-m%E1%BB%9Bi-hai-n%C6%B0%E1%BB%9Bc-l%C3%A0o-v%C3%A0-campuchi/852722470225868/", #lấy được thông qua lấy id post
        "https://www.facebook.com/story.php/?story_fbid=860048816159900&id=100064643681682", #lấy được thông qua lấy id post
        "https://www.facebook.com/photo.php?fbid=828579469306835&id=100064643681682&set=a.249070910591030", #lấy id post qua id photo
        "https://www.facebook.com/longantv/videos/h%E1%BB%99i-ngh%E1%BB%8B-qu%C3%A1n-tri%E1%BB%87t-b%C3%A0i-vi%E1%BA%BFt-c%E1%BB%A7a-t%E1%BB%95ng-b%C3%AD-th%C6%B0-nguy%E1%BB%85n-ph%C3%BA-tr%E1%BB%8Dng/844661637484682/",
        "https://www.facebook.com/KCrushbetterthanyourcrush/photos/t%E1%BA%A1o-trend-%C4%91i-t%C3%ACm-kho-b%C3%A1u-b%C3%A0-tr%C6%B0%C6%A1ng-m%E1%BB%B9-lan-gi%E1%BA%A5u-ngo%C3%A0i-bi%E1%BB%83n-coi-ch%E1%BB%ABng-vi-ph%E1%BA%A1m-ph%C3%A1p/752982493609413/",
        "https://www.facebook.com/BBCnewsVietnamese/posts/821651650001114/?comment_id=440373208660950",
                 
    ] 
    list_link = [
        "https://m.facebook.com/story.php/?story_fbid=784809087018564&id=100064684400850",
        "https://www.facebook.com/photo.php?fbid=677057377759224&id=100063649042107&set=a.280171060781193&locale=uk_UA",
        "https://www.facebook.com/PTTHHANAM/videos/c%C3%A1c-c%C6%A1-quan-%C4%91%C6%A1n-v%E1%BB%8B-%C4%91%E1%BB%8Ba-ph%C6%B0%C6%A1ng-t%E1%BB%95-ch%E1%BB%A9c-h%E1%BB%8Dc-t%E1%BA%ADp-qu%C3%A1n-tri%E1%BB%87t-gi%C3%A1-tr%E1%BB%8B-%C3%BD-ngh%C4%A9a-n%E1%BB%99i-dun/1370255207020624/",
        "https://m.facebook.com/BBCnewsVietnamese/photos/c%C3%A1c-%C4%91%E1%BB%93ng-ch%C3%AD-c%E1%BB%A9-ch%E1%BB%9D-xemng%C3%A0y-1352023-%C4%91%E1%BA%A1i-bi%E1%BB%83u-qu%E1%BB%91c-h%E1%BB%99i-nguy%E1%BB%85n-ph%C3%BA-tr%E1%BB%8Dng-%C4%91%C3%A3-c%C3%B3-bu%E1%BB%95/828767002622912/",
    ]
    sc = ScraperInfoPost()
    sc.start_get_info(datasets=list_link)
    

if __name__ == "__main__":
    #main_search_post_fb()
    main_get_post_from_link()