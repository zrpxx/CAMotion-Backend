import json
import requests

def get_channelkey(user_id: int, camera_id: int):
    # 请求地址
    url = "http://zrp.cool:8090/control/get?room=%d_%d" % (user_id, camera_id)
    response = requests.get(url)
    channelkey = "Failed"
    if response.status_code == 200:
        # 获取相应内容
        response = response.json()
        channelkey = response.get('data')
    else:
        print("Failed")
    return channelkey
