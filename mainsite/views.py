# -*- coding: utf-8 -*-

from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from datetime import datetime

# Create your views here.
def homepage(request):
	tempalte = get_template('index.html')
	posts = Post.objects.all()
	now = datetime.now()
	html = tempalte.render(locals())
	return HttpResponse(html)

def showpost(request, slug):
	template = get_template('post.html')
	try:
		post = Post.objects.get(slug=slug)
		if post != None:
			html = template.render(locals())
			return HttpResponse(html)
	except:
		return redirect('/')
