from django.contrib import admin
from .models import Log

# Register your models here.
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'object_id', 'created_at')
    list_filter = ('action', 'model_name', 'created_at')
    search_fields = ('user__username', 'model_name', 'description')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'description', 'changes', 'ip_address', 'user_agent')