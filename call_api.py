import requests
import json


phrase = 'chủ tịch quốc hội vương đình huệ'
time_start = '2024-04-24' #Format YYYY-MM-DD


api_address=f'http://192.168.143.53:5000/api/search?phrase={phrase}&time_start={time_start}'


# Gửi GET request đến API
print('Sending request .........')
response = requests.get(api_address,timeout=3600)

# Kiểm tra mã trạng thái của response
if response.status_code == 200:
    # Lấy phản hồi JSON từ response
    data = response.json()
    with open("result.json", "w") as json_file:
        json.dump(data, json_file)
else:
    print('Request failed with status code:', response.status_code)