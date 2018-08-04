# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def main_deal(request):
	try:
		webData = request.body
		xmlData = ET.fromstring(webData)

		msg_type = xmlData.find('MsgType').text
		ToUserName = xmlData.find('ToUserName').text
		FromUserName = xmlData.find('FromUserName').text
		CreateTime = xmlData.find('CreateTime').text
		MsgType = xmlData.find('MsgType').text
		MsgId = xmlData.find('MsgId').text

		toUser = FromUserName
		fromUser = ToUserName

		if msg_type == 'text':
			content = "文字"
			replyMsg = TextMsg(toUser, fromUser, content)
			return replyMsg.send()

		elif msg_type == 'image':
			content = "图片"
			replyMsg = TextMsg(toUser, fromUser, content)
			return replyMsg.send()

		elif msg_type == 'voice':
			content = "语音"
			replyMsg = TextMsg(toUser, fromUser, content)
			return replyMsg.send()

		elif msg_type == 'video':
			content = "视频"
			replyMsg = TextMsg(toUser, fromUser, content)
			return replyMsg.send()

		elif msg_type == 'shortvideo':
			content = "小视频"
			replyMsg = TextMsg(toUser, fromUser, content)
			return replyMsg.send()

		elif msg_type == 'location':
			content = "位置"
			replyMsg = TextMsg(toUser, fromUser, content)
			return replyMsg.send()

		else:
			msg_type == 'link'
			content = "链接"
			replyMsg = TextMsg(toUser, fromUser, content)
			return replyMsg.send()

	except Exception, Argment:
		return Argment

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
