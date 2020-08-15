from django.contrib import admin
from .models import Question, Choice

admin.site.site_header = 'Poll Site'
admin.site.site_titel = 'Poll Admin Area'
admin.site.index_title = 'Welcome to poll admin area'

admin.site.register(Question)
admin.site.register(Choice)
