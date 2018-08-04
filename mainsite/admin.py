# -*- coding: utf-8 -*-
from .models import Post

from django.contrib import admin

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'pub_date')

admin.site.register(Post, PostAdmin)

