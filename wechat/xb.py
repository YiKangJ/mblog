# encoding=utf-8
import requests
import time
import json

def chat(words):
	url = "https://weibo.com/aj/message/add?ajwvr=6"

	url_get = "https://m.weibo.cn/msg/messages?uid=5175429989&page=1"

	params = {
				"__rnd": int(round(time.time()*1000)),
				"location": "msgdialog",
				"module": "msgissue",
				"style_id": "1",
				"text": words,
				"uid": "5175429989",
				"tovfids": "",
				"fids": "",
				"el": "[object HTMLDivElement]",
				"_t": "0"
	}

	headers = {
				"Host": "weibo.com",
				"Connection": "keep-alive",
				"Content-Length": "125",
				"Origin": "https://weibo.com",
				"X-Requested-With": "XMLHttpRequest",
				"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
				"Content-Type": "application/x-www-form-urlencoded",
				"Accept": "*/*",
				"Referer": "https://weibo.com/message/history?uid=5175429989&name=%E5%B0%8F%E5%86%B0",
				"Accept-Encoding": "gzip, deflate, br",
				"Accept-Language": "zh-CN,zh;q=0.9",
				"Cookie":"SINAGLOBAL=1467533527804.976.1522628997152; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5gPBaG1IlxaTjGDcHiekGP5JpX5KMhUgL.FozN1hnpeK-peoe2dJLoIEXLxKqLBoML1KnLxKqLBoML1KnLxKML1-2L1hBLxKnL1-zL12zLxKnL1-zL12zt; UM_distinctid=162eaf9addb221-0e3ec03e85fd0e-3b7c015b-100200-162eaf9addc89f; YF-Ugrow-G0=ea90f703b7694b74b62d38420b5273df; ALF=1556175897; SSOLoginState=1524639898; SCF=ApN27auLlpddKW2xFc4xZxqADLiicy3bZlpx8xckZgeoNQpOie5qVE_y0p_qrlY26Fdosf52ysHE-OhPCvUeP1I.; SUB=_2A2535FjKDeRhGeRJ41oQ8SvNyT-IHXVUkM0CrDV8PUNbmtBeLWnMkW9NTeuaXxGz3r9Mqp7A0ox-I5LAokaJQSjq; SUHB=0cS3AjXy2pKkF6; wvr=6; YF-V5-G0=82f55bdb504a04aef59e3e99f6aad4ca; YF-Page-G0=d30fd7265234f674761ebc75febc3a9f; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=2245083023345.0557.1524639903621; ULV=1524639903676:9:9:4:2245083023345.0557.1524639903621:1524528845593"
	}

	headers_get = {
					"Accept": "text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8",
					"Accept-Encoding": "gzip, deflate, br",
					"Accept-Language": "zh-CN,en-US;q=0.7,en;q=0.3",
					"Connection": "keep-alive",
					"Cookie": "_T_WM=c0897b9fab8301f85b4da15c61e9918a; ALF=1527231898; SCF=ApN27auLlpddKW2xFc4xZxqADLiicy3bZlpx8xckZgeoesk56071LfqWQm6NERt16DtijaamssE6I2SuNTCsHj0.; SUB=_2A2535Fj-DeRhGeRJ41oQ8SvNyT-IHXVVJ3i2rDV6PUJbktANLRLBkW1NTeuaX0NzRak_HKKQysbuJxE67qEBdQBh; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5gPBaG1IlxaTjGDcHiekGP5JpX5K-hUgL.FozN1hnpeK-peoe2dJLoIEXLxKqLBoML1KnLxKqLBoML1KnLxKML1-2L1hBLxKnL1-zL12zLxKnL1-zL12zt; SUHB=0z1QInhhDK16MS; SSOLoginState=1524639918",
					"Host": "m.weibo.cn",
					"Upgrade-Insecure-Requests": "1",
					"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

	requests.post(url, data=params, headers=headers)
	try_times = 0
	while try_times < 20:
		res = requests.get(url_get, headers=headers_get)
		#	print res.status_code
		if res.status_code != 200:
			return "服务器错误！"
		res = res.text
		msgs = json.loads(res)
		if msgs['ok'] != 1:
			return '消息错误！'
		data = msgs['data']
		for i in range(len(data)):
			if data[0]['recipient_id'] == 2788115123:
				text = data[0]['text']
				return text
			break
	return '响应超时，请重新发送！'

if __name__ == "__main__":
	print chat("ceshi")
