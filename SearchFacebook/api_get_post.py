from requests import Session
from SearchFacebook.define_api import *
def get_infor_posts_page_from_api(storyID: str, session: Session = None):
    try:
        data = {
            'av': '',
            '__user': '',
            '__a': '1',
            '__comet_req': '15',
            'fb_dtsg': 'NAcMm4E0lcQC8DNeO4otqK6dkDMADS0jRFpnJTxpy6rk7DjpH6SYjaA:2:1710219296',
            'jazoest': '25328',
            'lsd': 'BsQuJc5kRmhQebv0VOsHcH',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometSinglePostContentQuery',
            'variables': '{"feedbackSource":2,"feedLocation":"PERMALINK","focusCommentID":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"permalink","scale":1,"storyID":"' + storyID + '","useDefaultActor":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__StoriesTrayShouldShowMetadatarelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false}',
            'server_timestamps': 'true',
            'doc_id': '6429441107159285',
        }
        if session:
            response = session.post(API_URL, data=data, timeout=TIME_OUT)
        else:
            print(f"Warning >> session is None ")
            return None
        return response.text
    except Exception as e:
        print(f"Error func get_infor_posts_group_from_api: {e}")
        return None
    
def get_infor_post_group(session: Session, groupID: str, storyID: str):
    try:
        if storyID and groupID:
            data = {
                'av': '',
                '__user': '',
                '__a': '1',
                '__comet_req': '15',
                'fb_dtsg': 'NAcOyerE6mxRWxDB2tec0dwDeC28OzTNsiwM6EeTGIDCrR6HOj98ymg:2:1710219296',
                'jazoest': '25410',
                'lsd': 'BwgDP_dgC_fNpBzBh2kK8f',
                'qpl_active_flow_ids': '431626709',
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CometGroupPermalinkRootContentFeedQuery',
                'variables': '{"feedbackSource":2,"feedLocation":"DEDICATED_COMMENTING_SURFACE","focusCommentID":null,"groupID":"' + groupID + '","privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"group_permalink","scale":1,"storyID":"' + storyID + '","useDefaultActor":false,"__relay_internal__pv__GroupsCometGroupChatLazyLoadLastMessageSnippetrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__StoriesTrayShouldShowMetadatarelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false}', 
                #'variables': '{"feedbackSource":2,"feedLocation":"GROUP_PERMALINK","focusCommentID":null,"groupID":"' + groupID + '","privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"group_permalink","scale":1,"storyID":"' + storyID + '","useDefaultActor":false,"__relay_internal__pv__GroupsCometGroupChatLazyLoadLastMessageSnippetrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__StoriesTrayShouldShowMetadatarelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false}',
                'server_timestamps': 'true',
                'doc_id': '7427501437309006',
            }
            if session:
                response = session.post(API_URL, data=data, timeout=TIME_OUT)
            else:
                print(f"Warning >> session is None ")
                return None
            # response = requests.post(API_URL, headers=HEADERS, data=data)
            return response.text
    except Exception as e:
        print(e)
        return None