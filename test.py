import requests

url = 'http://127.0.0.1:8000/create_log/'
params = {
    "camera_id": 53,
    "info": "string",
    "delete_img": "string",
    "img_url": "string"
}
requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接
req2 = requests.post(url, json=params)
print(req2.json())
