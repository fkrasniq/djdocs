from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to restrict class-based views to users with specific roles.
    
    Usage:
        class TeacherDashboard(RoleRequiredMixin, TemplateView):
            allowed_roles = ['teacher', 'admin']
            template_name = 'teacher_dashboard.html'
    
    Attributes:
        allowed_roles (list): List of role slugs or names that can access the view
        require_active_role (bool): If True, checks active_role instead of any assigned role
    """
    allowed_roles = []  # Override in subclass
    require_active_role = False  # Set to True to check active role only
    
    def test_func(self):
        """
        Test if user has required role.
        
        Returns:
            bool: True if user can access, False otherwise
        """
        user = self.request.user
        
        # Superusers always pass
        if user.is_superuser:
            return True
        
        # No roles specified means no restriction
        if not self.allowed_roles:
            return True
        
        # Check active role if required
        if self.require_active_role:
            return self._check_active_role(user)
        
        # Check any assigned role
        return any(user.has_role(r) for r in self.allowed_roles)
    
    def _check_active_role(self, user):
        """Check if user's active role matches allowed roles."""
        # Check session first
        active_role = None
        role_id = self.request.session.get('active_role_id')
        if role_id:
            active_role = user.roles.filter(pk=role_id).first()
        
        # Fall back to database
        if not active_role:
            active_role = getattr(user, 'active_role', None)
        
        if not active_role:
            return False
        
        # Check if active role matches
        return any(
            active_role.slug.lower() == r.lower() or 
            active_role.name.lower() == r.lower() 
            for r in self.allowed_roles
        )
    
    def handle_no_permission(self):
        """
        Handle case when user doesn't have permission.
        
        Override to customize behavior (e.g., show custom message).
        """
        raise PermissionDenied(
            f"You need one of these roles: {', '.join(self.allowed_roles)}"
        )


class ActiveRoleRequiredMixin(RoleRequiredMixin):
    """
    Convenience mixin that requires active role (not just assigned role).
    
    Usage:
        class TeacherOnlyView(ActiveRoleRequiredMixin, TemplateView):
            allowed_roles = ['teacher']
            template_name = 'teacher_view.html'
    """
    require_active_role = True


class MultiRoleViewMixin:
    """
    Mixin to provide different behaviors based on user's active role.
    
    Usage:
        class DashboardView(MultiRoleViewMixin, TemplateView):
            role_templates = {
                'teacher': 'teacher_dashboard.html',
                'student': 'student_dashboard.html',
                'admin': 'admin_dashboard.html',
            }
            default_template = 'generic_dashboard.html'
    """
    role_templates = {}
    default_template = None
    
    def get_template_names(self):
        """Get template based on user's active role."""
        user = self.request.user
        
        if not user.is_authenticated:
            return [self.default_template] if self.default_template else super().get_template_names()
        
        # Get active role
        active_role = None
        role_id = self.request.session.get('active_role_id')
        if role_id:
            active_role = user.roles.filter(pk=role_id).first()
        
        if not active_role:
            active_role = getattr(user, 'active_role', None)
        
        # Get template for role
        if active_role:
            role_key = active_role.slug.lower()
            if role_key in self.role_templates:
                return [self.role_templates[role_key]]
        
        # Fall back
        if self.default_template:
            return [self.default_template]
        
        return super().get_template_names()
