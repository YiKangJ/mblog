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
from xb import chat

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
                back = ''
                if names:
                    for i in range(len(scores)):
                        if scores[i] != '':
                            back += names[i]+'\t'+scores[i]+'\n'
                    content = back
                else:
                    content = chat(content) 
            elif content.isdigit():
                back = express(content)
                if back == 'error':
                    content = chat(content)
                else:
                    content = back 
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
            content = chat(content)
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

if __name__ == "__main__":
    pass
