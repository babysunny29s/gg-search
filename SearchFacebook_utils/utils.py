import json
import base64
import re
from post import Post
from datetime import datetime
def decode_base64(encoded_string: str):
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        print(e)
        return None
def encode_base64(input_string):
    try:
        encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
        encoded_string = encoded_bytes.decode('utf-8')
        return encoded_string
    except Exception as e:
        print("Error encoding Base64:", str(e))
        return None

def get_id_author_from_id_encode(input_string):
    decoded_string = decode_base64(input_string)
    if decoded_string:
        try:
            decoded_string = decoded_string.replace('S:_I', '')

            id_ = decoded_string.split(":")[0]
            return id_
        except Exception as e:
            print(e)
            return None
def write_log_json_post(post : Post, file = ""):
    data = post.__dict__
    if file == "":
        file = "logPost.json"
    print(f"write data to file {file}")
    with open(file, "a", encoding="utf-8") as fp:
        json.dump(data, fp)
        fp.write("\n")
def check_time_line_expired(timestamp, timeline):
    print(f"Check timestamp expired {timeline}")
    date_time_from_timestamp = datetime.fromtimestamp(int(timestamp))
    if date_time_from_timestamp < timeline:
        return True
    else:
        return False
def get_id_post_from_id_encode(input_string):
    decoded_string = decode_base64(input_string)
    if decoded_string:
        try:
            decoded_string = decoded_string.replace('S:_I', '')

            id_ = decoded_string.split(":")[-1]
            return id_
        except Exception as e:
            print(e)
            return None