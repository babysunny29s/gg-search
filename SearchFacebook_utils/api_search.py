from requests import Session
from SearchFacebook.define_api import *
import requests

def get_data_post_search(text: str, session: Session = None, cursor = ""):
    try:
        data = {
            # 'av': '',
            # '__user': '',
            # '__a': '1',
            # '__comet_req': '15',
            # 'fb_dtsg': 'NAcMm4E0lcQC8DNeO4otqK6dkDMADS0jRFpnJTxpy6rk7DjpH6SYjaA:2:1710219296', # Anti-CSRF Token của Facebook – dùng để chặn hình thức tấn công CSRF
            # 'jazoest': '25328',
            # 'lsd': 'BsQuJc5kRmhQebv0VOsHcH',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'SearchCometResultsPaginatedResultsQuery',
            'variables': '{"allow_streaming":false,"args":{"callsite":"COMET_GLOBAL_SEARCH","config":{"exact_match":false,"high_confidence_config":null,"intercept_config":null,"sts_disambiguation":null,"watch_config":null},"context":{"bsid":"d55b3d3b-4607-423f-8498-42589d679812","tsid":null},"experience":{"client_defined_experiences":[],"encoded_server_defined_params":null,"fbid":null,"type":"POSTS_TAB"},"filters":["{\\"name\\":\\"recent_posts\\",\\"args\\":\\"\\"}"],"text":"' + text +'"},"count":5,"cursor":"' + cursor + '","feedLocation":"SEARCH","feedbackSource":23,"fetch_filters":true,"focusCommentID":null,"locale":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"search_results_page","scale":1,"stream_initial_count":0,"useDefaultActor":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__StoriesTrayShouldShowMetadatarelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false,"__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider":false}',
            'server_timestamps': 'true',
            'doc_id': '7862194793831603',
        }
        if session:
            response = session.post(API_URL, data=data, timeout=TIME_OUT)
        else:
            print(f"Warning >> session is None ")
            return None
        return response.text
    except Exception as e:
        print(f"Error func get_data_post_search: {e}")
        return None