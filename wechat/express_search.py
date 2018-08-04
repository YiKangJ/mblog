#encoding:utf-8
import requests
import json
import time

def deal_time(timestamp_str):
	timestamp= float(timestamp_str)
	local_time = time.localtime(timestamp)
	return time.strftime("%Y-%m-%d %H:%M:%S", local_time)

def express(num):

    url = "https://sp0.baidu.com/9_Q4sjW91Qh3otqbppnN2DJv/pae/channel/data/asyncqury"
    params = {"appid": 4001, "nu": num}
    headers = { "Accept": "text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language":  "en-US,en;q=0.5",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": "BAIDUID=55ECBDBBDF5AB7284160F9…PX2ft0HPonHj8aDTQB3f; PSINO=1",
                "Host": "sp0.baidu.com",
                "Upgrade-Insecure-Requests": "1",
   	            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/58.0"}
    res = requests.get(url, params=params, headers=headers)
    res = json.loads(res.text)
    content = ''
    status = int(res['status'])
    if status == 0:
        context = res['data']['info']['context']
        for item in context:
            content += deal_time(item['time']) + ':' + item['desc'] + '\n'
        return content
    else:
        return "error"
if __name__ == "__main__":

    print express(789682342755)
