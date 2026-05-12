from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from .models import Log
from config.middleware import get_request
from django.contrib.auth.signals import user_logged_out
models = [
    ('inventory','MenuItem'),
    ('inventory','Resource'),
    ('inventory','MenuCategory'),
    ('inventory','MenuItemResource'),
    ('inventory','inventoryCategory'),
    ('inventory','Producer'),
    ('inventory','ResourceItem'),
    ('inventory','StorageLocation'),
    ('order','Order'),
    ('order','OrderItem'),
    ('users','User'),
    ('users','Role'),
    ('users','Permission'),
    ('table','Table'),
    ('table','Reservation'),
    ('table','Location'),
    ('hardware','Printer'),
    ('hardware','CashierPrinter'),
    ('hardware','PrinterJob'),
]
def track_models(sender):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    return (app_label, model_name.capitalize()) in models or \
           (app_label, sender._meta.object_name) in models
def get_model_changes(instance, original_data):
    changes = {}
    current_data= {}
    for field in instance._meta.get_fields():
        if field.many_to_one or field.one_to_one or not hasattr(field, 'attname'):
            continue
        try:
            current_data[field.name] = str(getattr(instance, field.name))
        except:
            continue
    
    for key, new_value in current_data.items():
        old_value = original_data.get(key)
        if old_value != new_value:
            changes[key] = {
                'old': old_value,
                'new': new_value
            }
    
    return changes
_original_data = {}
@receiver(pre_save)
def store_original_data(sender, instance, **kwargs):
    """Store original data before save to track changes"""
    if not track_models(sender):
        return
    
    if instance.pk:
        try:
            original_instance = sender.objects.get(pk=instance.pk)
            original_data = {}
            for field in sender._meta.get_fields():
                if field.many_to_one or field.one_to_one or not hasattr(field, 'attname'):
                    continue
                try:
                    original_data[field.name] = str(getattr(original_instance, field.name))
                except:
                    continue
            _original_data[id(instance)] = original_data
        except sender.DoesNotExist:
            _original_data[id(instance)] = {}
def get_client_ip(request):
    """Extract client IP from request"""
    if not request:
        return None
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
        return ip
    
    return request.META.get('REMOTE_ADDR')

@receiver(post_save)
def log_create_update(sender, instance, created, **kwargs):
    """Log model creation and updates"""
    if not track_models(sender):
        return
    
    try:
        request = get_request()
        user = request.user if request and request.user.is_authenticated else None
        ip_address = get_client_ip(request) if request else None
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500] if request else ''
        
        action = 'CREATE' if created else 'UPDATE'
        
        # Get changes for UPDATE action
        changes = {}
        if not created:
            original_data = _original_data.pop(id(instance), {})
            changes = get_model_changes(instance, original_data)
        
        # Skip logging if no changes in UPDATE
        if not created and not changes:
            return
        
        description = f'{action} {sender._meta.verbose_name}: {str(instance)[:100]}'
        
        Log.objects.create(
            user=user,
            action=action,
            model_name=sender._meta.model_name,
            object_id=instance.pk,
            description=description,
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception as e:
        print(f'Error logging audit: {e}')
@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    """Log model deletion"""
    if not track_models(sender):
        return
    
    try:
        request = get_request()
        user = request.user if request and request.user.is_authenticated else None
        ip_address = get_client_ip(request) if request else None
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500] if request else ''
        
        description = f'DELETE {sender._meta.verbose_name}: {str(instance)[:100]}'
        
        Log.objects.create(
            user=user,
            action='DELETE',
            model_name=sender._meta.model_name,
            object_id=instance.pk,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception as e:
        print(f'Error logging audit: {e}')


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    """Log user logout"""
    try:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        Log.objects.create(
            user=user,
            action='LOGOUT',
            model_name='User',
            description=f'User logout: {user.username}',
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception as e:
        print(f'Error logging logout: {e}')
    