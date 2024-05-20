import requests
from SearchFacebook.define_api import *
import json


def get_storyID_from_id_photo(session: requests.Session, id_photo: str):
    try:
        data = {
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometPhotoTagLayerQuery',
            'variables': '{"nodeID":"' + id_photo + '","scale":1}',
            'server_timestamps': 'true',
            'doc_id': '6540798456012927',
        }
        if session:
            response = session.post(API_URL, data=data, timeout=TIME_OUT)
            text = response.text.replace(' ', '')
            matchs = text.split("\n")
            #print(matchs)
            for match in matchs:
                if "CometPhotoTagLayerQuery$defer$photo-tag-wrapper" in match:
                    data = json.loads(match)
                    storyID = data["data"]['creation_story']['id']
                    if storyID:
                        return storyID
                    else:
                        return None
        else:
            print(f"Warning >> session is None ")
            return None
        # # response = requests.post(API_URL, headers=HEADERS, data=data)
        # return response.text
    except Exception as e:
        print(e)
        return None
    
# ss = requests.Session()
# print(get_storyID_from_id_photo(session=ss, id_photo="677057377759224"))