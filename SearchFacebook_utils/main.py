# from api_search import get_data_post_search
# import requests
# from define_api import *
from scraper_post_search import ScraperPostSearch
import os
from datetime import datetime, timedelta
# ss = requests.session()
# ss.headers.update(HEADERS)
# results = get_data_post_search(session=ss, text="nguyễn văn chiến")
# print(results)


# with open("response.txt", "w", encoding="utf-8") as fp:
#     fp.write(results)
if not os.path.exists("db/Search"):
    os.makedirs("db/Search")

def main():
    # print(
        
    # "\n                    _oo0oo_                      \n"
    # "                   o8888888o                       \n"
    # "                   88' . '88                       \n"
    # "                   (| -_- |)                       \n"
    # "                   0\  =  /0                       \n"
    # "                 ___/`---'\___                     \n"
    # "               .' \\|     |// '.                   \n"
    # "              / \\|||  :  |||// \                  \n"
    # "             / _||||| -:- |||||- \                 \n"
    # "            |   | \\\  -  /// |   |                \n"
    # "            | \_|  ''\---/''  |_/ |                \n"
    # "             \ .-\__  '-' ___/-. /                 \n"
    # "           ___'. .' /--.--\ `. .'___               \n"
    # "        ."" '< `.___\_<|>_/___.' >' "".            \n"
    # "      | | :  `- \`.;`\ _ /`;.`/ - ` : | |          \n"
    # "      \  \ `_.   \_ __\ /__ _/   .-` /  /          \n"
    # "  =====`-.____`.___ \_____/___.-`___.-'=====       \n"
    # "                    `=---='                        \n"
    # "            It works … on my machine               \n"
    # "  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      \n"
 
    # )
    number_day_post = 1  #Thời gian lấy bài trong search, đơn vị ngày
    Max_post = 50   # Số post tối đa
    keyword = "Nguyễn Phú Trọng đốt lò" #Từ khóa search
    current_day = datetime.now()
    datetime_start = datetime(current_day.year, current_day.month, current_day.day, current_day.hour, current_day.minute, current_day.second)
    time_line = datetime_start - timedelta(days=number_day_post)
    print(f"==============TimeLine : {time_line}=================")
    sc = ScraperPostSearch(time_line=time_line, MAX_SIZE_POST=Max_post)
    sc.search_post(keyword=keyword)
    


if __name__ == "__main__":
    main()