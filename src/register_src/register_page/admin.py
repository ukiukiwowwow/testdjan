from django.contrib import admin
from django.utils.html import format_html
from .models import *


class PasswordInline(admin.TabularInline):
    model = Password
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    list_display = ['name']
    fieldsets = [
        (None,               {'fields': ['name']})
    ]
    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/register_page/student/{}/delete/">Delete</a>', obj.id)
    list_display = ('__str__', 'delete_button')
    inlines = [PasswordInline]
    search_fields = ['Password']

admin.site.register(Student, StudentAdmin)