import requests
import json

def get_channelkey(user_id: int,camera_id: int):
    # 请求地址
    url = "https://zrp.cool:8090/control/get?room=%d_%d" % (user_id, camera_id)
    response = requests.get(url)
    # 获取请求状态码 200为正常
    channelkey = "0"
    if (response.status_code == 200):
        # 获取相应内容
        content = response.text
        # json转数组（Py叫字典，我喜欢叫数组）
        json_dict = json.loads(content)
        json_list = json_dict['result']
        channelkey = json_list[0].get("data")

    return channelkey


