from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.db import transaction


@receiver(user_logged_in)
def ensure_active_role_on_login(sender, user, request, **kwargs):
    """
    Signal handler to ensure user's active_role is valid on login.
    
    Purpose:
        - Clears active_role if it was removed from user's assigned roles
        - Prevents stale role references
        - Maintains data integrity
    
    When triggered:
        - User logs in successfully
        - After authentication completes
    
    Actions:
        - Checks if user.active_role exists in user.roles
        - If not, sets active_role to None
        - Clears session active_role if invalid
    
    Configuration:
        Signals are auto-discovered if:
        1. This file is imported in accounts/apps.py:
        
           class AccountsConfig(AppConfig):
               name = 'accounts'
               
               def ready(self):
                   import accounts.signals
        
        2. Or imported in accounts/__init__.py:
        
           default_app_config = 'accounts.apps.AccountsConfig'
    """
    # Check database active_role
    active_role = getattr(user, 'active_role', None)
    if active_role and not user.roles.filter(pk=active_role.pk).exists():
        # Active role was removed - clear it
        with transaction.atomic():
            user.active_role = None
            user.save(update_fields=['active_role'])
    
    # Check session active_role
    if hasattr(request, 'session'):
        role_id = request.session.get('active_role_id')
        if role_id and not user.roles.filter(pk=role_id).exists():
            # Session role was removed - clear it
            request.session.pop('active_role_id', None)
