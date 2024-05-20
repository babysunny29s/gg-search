import time
import uvicorn
import pickle
import re
import hashlib

import get_data

from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, BackgroundTasks
from kafka import KafkaProducer
from pydantic import BaseModel
from pymongo import MongoClient

from read_config import *
import tool_config 
from SearchGoogle.search_gg import *


app = FastAPI()
producer = KafkaProducer(bootstrap_servers=[tool_config.kafka_address])
kafka_topic = tool_config.kafka_topic
client = MongoClient(tool_config.mongodb_address)
db = client["request_db"]
collection = db["request_collection"]



class SearchRequest(BaseModel):
    id: str
    phrase: str
    channel: list
    time_start: str
    
    
@app.get("/")
async def root():
    return {"message": "Hello World"}  

@app.post("/api/search")
async def receiver_new_task(request: SearchRequest, background_tasks: BackgroundTasks):
    id = request.id
    phrase = request.phrase
    channel = request.channel
    time_start = request.time_start

    # Kiểm tra xem đã đạt đến giới hạn số lượng yêu cầu trong khoảng thời gian đã cho hay chưa
    if not is_allowed_request():
        raise HTTPException(status_code=429, detail="Too Many Requests")
    
    # Kiểm tra channel là một danh sách
    if isinstance(channel, list):
        # Kiểm tra phrase là một chuỗi
        if isinstance(phrase, str):
            # Kiểm tra time_start có đúng định dạng YYYY-MM-DD
            if re.match(r"\d{4}-\d{2}-\d{2}", time_start):
                # time_sent = datetime.now()
                # time_sent_str = time_sent.strftime("%Y-%m-%d %H:%M:%S")
                # input_string = phrase + time_start + time_sent_str
                # id = hashlib.md5(input_string.encode()).hexdigest()
                background_tasks.add_task(process_data, id , phrase, channel, time_start)
                return {"status_code": 200, "message": "The request was sent successfully", "id" : id}
            else:
                raise HTTPException(status_code=400, detail="Invalid time_start format. Expected format: YYYY-MM-DD")
        else:
            raise HTTPException(status_code=400, detail="Invalid phrase parameter. Expected string.")
    else:
        raise HTTPException(status_code=400, detail="Invalid channel parameter. Expected list.")

    # if phrase and time_start:
    #     background_tasks.add_task(process_data, phrase, channel, time_start)
    #     return {"status_code": 200, "message": "The request was sent successfully"}
    # else:
    #     raise HTTPException(status_code=400, detail="Invalid request parameters")

def process_data(id, phrase, channel, start_time):
    try:
        all_data_post = {}
        # GET YOUTUBE
        start = time.time()
        if 'tiktok' in channel:
            data_post_tiktok = get_data.search_and_getinfo_tiktok(phrase, start_time)
        else:
            data_post_tiktok = []
        if 'facebook' in channel:
            data_post_facebook = get_data.search_and_getinfo_facebook(phrase, start_time)
        else:
            data_post_facebook = []
        if 'youtube' in channel:
            data_post_youtube = get_data.search_and_getinfo_youtube(phrase, start_time)
        else:
            data_post_youtube = []
        all_data_post["facebook"] = data_post_facebook
        all_data_post["tiktok"] = data_post_tiktok
        all_data_post["youtube"] = data_post_youtube
        time_done = time.time()
        document = {
            'id': id,
            'phrase': phrase,
            'time_start': start_time,
            'data_posts': all_data_post,
            'time_done_crawl': time_done,  
            'time_start_crawl': start
        }
        with open("output.json", "w") as file:
            json.dump(document, file)
        push_kafka(topic=kafka_topic, obj=document)
        end = time.time()
        logger.info(f"Time to trace phrase is {end-start}")
    except Exception as e:
        logger.error(e)

def is_allowed_request():
    # Tạo query để tìm kiếm số lượng yêu cầu trong khoảng thời gian hiện tại
    current_hour_start = datetime.now().replace(minute=0, second=0, microsecond=0)
    current_hour_end = current_hour_start + timedelta(hours=1)
    query = {
        "timestamp": {"$gte": current_hour_start, "$lt": current_hour_end}
    }

    # Đếm số lượng yêu cầu trong khoảng thời gian hiện tại
    request_count = collection.count_documents(query)

    if request_count < 20:
        # Nếu số lượng yêu cầu chưa đạt giới hạn, thêm yêu cầu mới vào cơ sở dữ liệu
        collection.insert_one({"timestamp": datetime.now()})
        return True
    else:
        # Nếu đã vượt quá giới hạn, từ chối yêu cầu
        return False
    
def push_kafka(topic, obj):
    # logger.info("push kafka")
    bytes_obj = pickle.dumps([obj])
    producer.send(topic, bytes_obj)
    producer.flush()
    logger.info("done push kafka")
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=15000)