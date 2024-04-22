# from requests_html import HTMLSession
import re
from SearchFacebook.define_api import *
from requests import Session
# headers = {
#     'accept': '*/*',
#     'accept-language': 'vi,vi-VN;q=0.9,en-US;q=0.8,en;q=0.7',
#     'content-type': 'application/x-www-form-urlencoded',
#     # 'cookie': 'ps_l=0; ps_n=0; sb=bLryZSZYtNRMTiWLrq4mvaXg; datr=bLryZSvliNsxWojCTK47lxVV; c_user=100029097677957; wd=1920x945; xs=10%3A-9EkPExfRXL9SQ%3A2%3A1710409673%3A-1%3A6351%3A%3AAcXjRWr1Yeqg-siYWekCufa84DssURZ9BDsa6owaYTI; fr=1J3UT1BZiYrJ9iVkY.AWWvABE49vvPkQKEiwgihmPAIgI.BmHdac..AAA.0.0.BmHdae.AWXZvaiHmYg; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1713231768401%2C%22v%22%3A1%7D',
#     'dpr': '1',
#     # 'origin': 'https://www.facebook.com',
#     # 'referer': 'https://www.facebook.com/profile.php?id=100029097677957&sk=groups_member',
#     'sec-ch-prefers-color-scheme': 'light',
#     'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
#     'sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.106", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.106"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-model': '""',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-ch-ua-platform-version': '"15.0.0"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#     'viewport-width': '1920',
#     # 'x-asbd-id': '129477',
#     # 'x-fb-friendly-name': 'ProfileCometAppCollectionListRendererPaginationQuery',
#     # 'x-fb-lsd': '_H1VEAePrIkpUuqnYy1kMG',
# }
# # cookies = {
# #     'ps_l': '0',
# #     'ps_n': '0',
# #     'sb': 'bLryZSZYtNRMTiWLrq4mvaXg',
# #     'datr': 'bLryZSvliNsxWojCTK47lxVV',
# #     'c_user': '100029097677957',
# #     'wd': '1920x945',
# #     'xs': '10%3A-9EkPExfRXL9SQ%3A2%3A1710409673%3A-1%3A6351%3A%3AAcXjRWr1Yeqg-siYWekCufa84DssURZ9BDsa6owaYTI',
# #     'fr': '1J3UT1BZiYrJ9iVkY.AWWvABE49vvPkQKEiwgihmPAIgI.BmHdac..AAA.0.0.BmHdae.AWXZvaiHmYg',
# #     'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1713231768401%2C%22v%22%3A1%7D',
# # }
# pattern_storyID = r'(?<="storyID":")[^"]+'
# pattern_groupID = r'(?<="groupID":")(\d+)'
# session = HTMLSession()
# session.headers.update(headers)
# response = session.get('https://www.facebook.com/nguyenhoan2711/posts/pfbid0zev9rEj9seWBdtGhrvqU42t3zt7SxrPPWu3XZgAdS8vVaavbiTcotyug4JRbLZVnl')
# storyID = list(set(re.findall(pattern_storyID, response.text)))
# groupID = list(set(re.findall(pattern_groupID, response.text)))
# scripts = response.html.find('script')
# with open("html.txt", "w", encoding="utf-8") as f:
#     f.write(response.text)
# ufi2_config_script = None

# for script in scripts:
#     if 'UFI2Config' in script.text:
#         ufi2_config_script = script.text
#         break

# if ufi2_config_script:
#     print("UFI2Config script found:")
#     print(ufi2_config_script)
#     with open("ufi2.txt", "w") as fp:
#         fp.write(response.text)

# else:
#     print("UFI2Config script not found")

def get_id_post(url, session: Session):
    pattern_storyID = r'(?<="storyID":")[^"]+'
    pattern_groupID = r'(?<="groupID":")(\d+)'
    try:
        response = session.get(url=url, timeout=TIME_OUT)
        storyID = list(set(re.findall(pattern_storyID, response.text)))
        groupID = list(set(re.findall(pattern_groupID, response.text)))
        if storyID:
            if "group" in url:
                if groupID:
                    return storyID[0], groupID[0]
                else:
                    print("Không có group ID")
                    return "", ""
            else:
                return storyID[0], ""
        else:
            print("Không tìm thấy id bài post")
            return "", ""
    except Exception as e:
        print(e)
        return "", ""