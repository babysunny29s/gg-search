import json
import tool_config as cfg
from datetime import datetime, timedelta
from logger import logger



def read_config():
    with open(cfg.config_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    phrase = data.get("phrase") 
    phrase = phrase.lower()
    time_start = data.get("time_start")
    time_range = calculate_time_period(time_start)
    if isinstance(time_range, int):
        logger.info(f"Trace information about phrase {phrase} from {time_start}")
    else:
        logger.info("Invalid time period specified in the config.")
        return
    return phrase, time_range

    
def calculate_time_period(start_date):
    now = datetime.now()
    try:
        start_time = datetime.strptime(start_date, "%Y-%m-%d")
        end_time = now
        time_period = end_time - start_time
        return time_period.days
    except ValueError:
        return "Invalid date format"

    
def extract_time_period(period):
    now = datetime.now()
    if period == 'h':
        # time_param = '1 giờ qua'
        start_time = now - timedelta(hours=1)
        end_time = now
    elif period == 'd':
        # time_param = '1 ngày trước'
        start_time = now - timedelta(days=1)
        end_time = now
    elif period == 'w':
        # time_param = '1 tuần trước'
        start_time = now - timedelta(weeks=1)
        end_time = now
    elif period == 'y':
        # time_param = '1 năm trước'
        start_time = now - timedelta(years=1)
        end_time = now
    else:
        return "Invalid parameter"
    return (start_time, end_time)


# test = read_config()
# print(test)
    