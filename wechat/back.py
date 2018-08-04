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

@csrf_exempt
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
		content += date + '\n'+weather + '\n'+ wind + '\n' + temp + '\n'
	return content

@csrf_exempt
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
			content = "text"
			replyMsg = TextMsg(toUser, fromUser, content)
			return replyMsg.send()

		elif msg_type == 'event':
			event = xmlData.find('Event').text
			if event == 'subscribe':
				replyMsg = EventMsg(toUser, fromUser)
				# replyMsg = TextMsg(toUser, fromUser, event)
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
		return replyMsg.send() #Argment

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
		<MsgType><![CDATA[text]]></MsgType>
		<Content><![CDATA[666666]]></Content>
		</xml>
		"""
		return XmlForm.format(**self.__dict)
