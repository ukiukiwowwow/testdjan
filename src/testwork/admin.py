from django.contrib import admin
from django.utils.html import format_html

from .models import *
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class AnswerInline(admin.TabularInline):
    model= Answer
    extra = 1

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/testwork/problem/{}/delete/">Delete</a>', obj.id)
    list_display = ('__str__', 'delete_button')
    inlines = [ChoiceInline,AnswerInline]
    list_filter = ["pub_date"]
    search_fields = ['title']

admin.site.register(Problem,ProblemAdmin)