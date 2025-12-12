from django.contrib.auth.decorators import user_passes_test
from functools import wraps


def has_roles(*roles):
    """
    Decorator to restrict access to users with specific roles.
    
    Usage:
        @has_roles('admin', 'manager')
        def my_view(request):
            pass
    
    Args:
        *roles: Role slugs or names to check
    
    Returns:
        Decorator function that checks if user has any of the specified roles
    
    Notes:
        - Superusers always pass
        - Case-insensitive role matching
        - User must be authenticated
    """
    def tester(user):
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return any(user.has_role(r) for r in roles)
    
    return user_passes_test(tester)


def require_role(role):
    """
    Decorator to require a single specific role.
    
    Usage:
        @require_role('teacher')
        def grade_students(request):
            pass
    """
    return has_roles(role)


def require_active_role(*roles):
    """
    Decorator to require active role matches one of the specified roles.
    
    Usage:
        @require_active_role('teacher', 'admin')
        def manage_class(request):
            pass
    
    Notes:
        - Checks active_role (not just assigned roles)
        - Useful for multi-role users who must have specific role active
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            
            if not user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                from django.shortcuts import resolve_url
                path = request.get_full_path()
                resolved_login_url = resolve_url('login')
                return redirect_to_login(path, resolved_login_url)
            
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check session active role first
            active_role = None
            role_id = request.session.get('active_role_id')
            if role_id:
                from .models import Role
                active_role = user.roles.filter(pk=role_id).first()
            
            # Fall back to database active role
            if not active_role:
                active_role = getattr(user, 'active_role', None)
            
            # Check if active role matches
            if active_role and any(
                active_role.slug.lower() == r.lower() or 
                active_role.name.lower() == r.lower() 
                for r in roles
            ):
                return view_func(request, *args, **kwargs)
            
            # Access denied
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You must have an active role to access this page.")
        
        return wrapper
    return decorator
