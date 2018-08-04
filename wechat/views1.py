# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.encoding import smart_str

import hashlib
import json
import requests
import xml.etree.ElementTree as ET
from express_search import express
from score import get_scores
import re
import time

# chat with xiao_ice
def chat(words):
	url = "https://weibo.com/aj/message/add?ajwvr=6"

	url_get = "https://m.weibo.cn/msg/messages?uid=5175429989&page=1"

	params = {
				"__rnd": int(time.time()),
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
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5083.400 QQBrowser/10.0.988.400",
				"Content-Type": "application/x-www-form-urlencoded",
				"Accept": "*/*",
				"Referer": "https://weibo.com/message/history?uid=5175429989&name=%E5%B0%8F%E5%86%B0",
				"Accept-Encoding": "gzip, deflate, br",
				"Accept-Language": "zh-CN,zh;q=0.9",
				"Cookie":"SINAGLOBAL=1467533527804.976.1522628997152; un=jinyikangjyk@qq.com; UOR=,,login.sina.com.cn; wvr=6; login_sid_t=9cace51a1e4aabbab7abd6411e618298; cross_origin_proto=SSL; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; YF-V5-G0=694581d81c495bd4b6d62b3ba4f9f1c8; WBStorage=85622cca475cfa2d|undefined; _s_tentry=-; Apache=5434148034369.499.1522652036990; ULV=1522652036998:3:3:3:5434148034369.499.1522652036990:1522629160640; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5gPBaG1IlxaTjGDcHiekGP5JpX5K2hUgL.FozN1hnpeK-peoe2dJLoIEXLxKqLBoML1KnLxKqLBoML1KnLxKML1-2L1hBLxKnL1-zL12zLxKnL1-zL12zt; ALF=1554188048; SSOLoginState=1522652049; SCF=ApN27auLlpddKW2xFc4xZxqADLiicy3bZlpx8xckZgeoWR5e3jcW62khpyy7L2D_OfPYZh3qNxrQsvGIEYEmnfU.; SUB=_2A253xaPBDeRhGeRJ41oQ8SvNyT-IHXVUspIJrDV8PUNbmtBeLU_jkW9NTeuaXxfsyO4RtTAwYgHlD8ZD69jwxyW2; SUHB=06ZVCkxKwXGTEs; YF-Page-G0=f70469e0b5607cacf38b47457e34254f"
	}

	headers_get = {
					"Accept": "text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8",
					"Accept-Encoding": "gzip, deflate, br",
					"Accept-Language": "zh-CN,en-US;q=0.7,en;q=0.3",
					"Connection": "keep-alive",
					"Cookie": "ALF=1525309702; SCF=AlEzZjcOx_VethlPt6Qn_TBt0vwnkYki66fs_gq0IT52xipjmo8Jg0EtAnmMSlosSLiR9muVjGjPKd1R7FhwwFw.; SUB=_2A253xqRXDeRhGeRJ41oQ8SvNyT-IHXVVSMwfrDV6PUNbktANLRL7kW1NTeuaX3iPgN9Nbsaf2B6tKUjgSzZ4CO7c; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5gPBaG1IlxaTjGDcHiekGP5JpX5KMhUgL.FozN1hnpeK-peoe2dJLoIEXLxKqLBoML1KnLxKqLBoML1KnLxKML1-2L1hBLxKnL1-zL12zLxKnL1-zL12zt; SUHB=0tK62FTd9p1f1p; _T_WM=d4daeac8484734cb22429ba93063d353",
					"Host": "m.weibo.cn",
					"Upgrade-Insecure-Requests": "1",
					"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/58.0"
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

# Create your views here.
@csrf_exempt
def weixin_main(request):
    if request.method == "GET":
        # 如果是GET请求，则为微信与服务器验证过程，获取相关参数，token等并返回相应参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        token = 'xinwei'
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashlib.sha1(hashstr.encode(encoding='utf-8')).hexdigest()
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('failed')
    else:
        othercontent = autoreply(request)
        return HttpResponse(othercontent)

def json_parse(json_dic):
    res = json_dic[0]
    city = res['currentCity']
    pm25 = res['pm25']
    data = res['weather_data']
    content = "{}天气预报\nPM2.5:{}\n".format(city, pm25)
    for weather_data in data:
        date = weather_data['date']
        weather = weather_data['weather']
        wind = weather_data['wind']
        temp = weather_data['temperature']
        # picUrl = weather_data['dayPictureUrl']
        content += date + '\n'+weather + '\n'+ wind + '\n' + temp + '\n'
    return content

def get_weather(locationX, locationY):
    url = "http://api.map.baidu.com/telematics/v3/weather?location={},{}&output=json&ak=xu5srr9UGMZZWnTEquS4jCbo".format(locationX,locationY)
    res = requests.get(url)
    res = json.loads(res.text)
    if res['error'] == 0:
        content = json_parse(res['results'])
    else:
        content = '无法获取当前位置天气'
    return content

@csrf_exempt
def autoreply(request):
    try:
        webData = request.body
        xmlData = ET.fromstring(webData)

        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        # CreateTime = xmlData.find('CreateTime').text
        # MsgType = xmlData.find('MsgType').text
        # MsgId = xmlData.find('MsgId').text

        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':
            content = xmlData.find('Content').text
            if '成绩' == content[0:2]:
                content_list = re.split('[_#|+\s\t\n]', content)
                username = content_list[1]
                password = content_list[2]
                names, scores = get_scores(username, password)
                content = ''
                if not names:
                    return "success"
                for i in range(len(scores)):
                    if scores[i] != '':
                        content += names[i]+'\t'+scores[i]+'\n'
                 
            elif content.isdigit():
                content = express(content)
                if content == 'error':
                    return "success" 
            else:
                content = chat(content)
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

        elif msg_type == 'image':
            # content = "图片"
            content = "success"
            # replyMsg = TextMsg(toUser, fromUser, content)
            return content #replyMsg.send()

        elif msg_type == 'voice':
            # content = "语音"
            content = "success"
            # replyMsg = TextMsg(toUser, fromUser, content)
            return content #replyMsg.send()

        elif msg_type == 'video':
            # content = "视频"
            content = "success"
            # replyMsg = TextMsg(toUser, fromUser, content)
            return content #replyMsg.send()

        elif msg_type == 'shortvideo':
            # content = "小视频"
            content = "success"
            #replyMsg = TextMsg(toUser, fromUser, content)
            return content #replyMsg.send()

        elif msg_type == 'location':
            x = float(xmlData.find('Location_X').text)
            y = float(xmlData.find('Location_Y').text)
            content = get_weather(y, x)
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        
        elif msg_type == 'event':
            event = xmlData.find('Event').text
            if event == "subscribe":
                replyMsg = EventMsg(toUser, fromUser)
#               replyMsg = TextMsg(toUser, fromUser, event)
                return replyMsg.send()
            else:
                content = "我会想你的～"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            # replyMsg = TextMsg(toUser, fromUser, event)
            # return replyMsg.send()

        else:
            # content = "链接"
            content = msg_type
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

    except Exception, Argment:
        replyMsg = TextMsg(toUser, fromUser, Argment)
        return replyMsg.send()

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

import time
class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)

class EventMsg(Msg):
    def __init__(self, toUserName, fromUserName):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        # self.__dict['Content'] = content
    def send(self):
         
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
        <item>
        <Title><![CDATA[\t欢迎关注！\n]]></Title> 
        <Description><![CDATA[1.回复任意内容对话小冰\n2.发送定位获取当地天气\n3.发送快递单号直接查询\n4.发送"成绩+学号+密码"获取成绩\n更多功能，敬请期待！]]></Description>
        <PicUrl><![CDATA[https://s17.postimg.org/kemp2xu4f/image.png]]></PicUrl>
        <Url><![CDATA[]></Url>
        </Articles>
        </xml>
        """
        return XmlForm.format(**self.__dict)
