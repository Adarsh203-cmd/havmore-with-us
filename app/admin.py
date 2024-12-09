from django.contrib import admin
from .models import usertable

@admin.register(usertable)
class UserTableAdmin(admin.ModelAdmin):
    list_display = ('email', 'cname', 'is_active', 'is_verified')
    search_fields = ('email', 'cname')
