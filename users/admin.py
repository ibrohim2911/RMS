from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Permission


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('name', 'pin', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'c_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'password1', 'password2', 'is_active'),
        }),
    )
    list_display = ('phone_number', 'name', 'role', 'is_active', 'is_superuser')
    list_filter = ('is_active', 'is_superuser', 'role')
    search_fields = ('phone_number', 'name')
    ordering = ('-c_at',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Permission)