from django.contrib import admin
from .models import Question, Choice

admin.site.site_header = 'Poll Site'
admin.site.site_titel = 'Poll Admin Area'
admin.site.index_title = 'Welcome to poll admin area'

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionFieldsetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Data Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionFieldsetAdmin)
# admin.site.register(Choice)
