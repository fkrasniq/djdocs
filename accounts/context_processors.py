def user_roles(request):
    """
    Context processor to inject user role information into all templates.
    
    Provides:
        - active_role: Current active Role object (session or DB)
        - user_roles: QuerySet of all roles assigned to user
        - Role-specific boolean flags for common roles
    
    Usage in templates:
        {% if is_teacher %}
            <a href="{% url 'grade_students' %}">Grade Students</a>
        {% endif %}
        
        {% if active_role %}
            Current role: {{ active_role.name }}
        {% endif %}
        
        {% for role in user_roles %}
            <span>{{ role.name }}</span>
        {% endfor %}
    
    Configuration:
        Add to settings.py:
        TEMPLATES = [{
            'OPTIONS': {
                'context_processors': [
                    ...
                    'accounts.context_processors.user_roles',
                ],
            },
        }]
    """
    if not request.user.is_authenticated:
        return {
            'active_role': None,
            'user_roles': [],
            'is_student': False,
            'is_teacher': False,
            'is_admin': False,
            'is_administrator': False,
            'is_manager': False,
            'is_employee': False,
            'is_director': False,
            'is_owner': False,
            'is_parent': False,
        }

    user = request.user
    active_role = None
    
    # Check session for ephemeral active role
    role_id = request.session.get('active_role_id')
    if role_id:
        active_role = user.roles.filter(pk=role_id).first()
        # Clean up if role was removed
        if not active_role:
            request.session.pop('active_role_id', None)
    
    # Fall back to database active role
    if not active_role:
        active_role = getattr(user, 'active_role', None)
    
    # Get role name for comparison
    role_name = active_role.name if active_role else None
    role_slug = active_role.slug if active_role else None
    
    return {
        'active_role': active_role,
        'user_roles': user.roles.all(),
        
        # Common role flags (case-insensitive)
        'is_student': _role_matches(role_name, role_slug, 'student'),
        'is_teacher': _role_matches(role_name, role_slug, 'teacher'),
        'is_admin': _role_matches(role_name, role_slug, 'admin'),
        'is_administrator': _role_matches(role_name, role_slug, 'administrator'),
        'is_manager': _role_matches(role_name, role_slug, 'manager'),
        'is_employee': _role_matches(role_name, role_slug, 'employee'),
        'is_director': _role_matches(role_name, role_slug, 'director'),
        'is_owner': _role_matches(role_name, role_slug, 'owner'),
        'is_parent': _role_matches(role_name, role_slug, 'parent'),
    }


def _role_matches(role_name, role_slug, target):
    """Helper to check if role matches target (case-insensitive)."""
    if not role_name:
        return False
    return (
        role_name.lower() == target.lower() or 
        (role_slug and role_slug.lower() == target.lower())
    )
