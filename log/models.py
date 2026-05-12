from django.db import models
from common.models import CommonModel
from django.contrib.auth import get_user_model
User = get_user_model()
class Log(CommonModel):
    
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('VIEW', 'View'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=255, help_text='Model affected by the action')
    object_id = models.PositiveIntegerField(null=True, blank=True, help_text='ID of the object affected')
    description = models.TextField(blank=True, help_text='Human-readable description of the action')
    changes = models.JSONField(default=dict, blank=True, help_text='Track old and new values')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
