from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'username', 'name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'name')}),
        ('Permissions', {'fields': ('is_admin', 'is_customer', 'is_creator', 'groups', 'user_permissions', 'email_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email', 'id')
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)
admin.site.register(Profile)
admin.site.register(Creator)