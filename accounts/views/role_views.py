from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from django.urls import reverse

from ..models import Role


# Define role-specific redirect targets
# Customize these URL names based on your project structure
REDIRECT_MAP = {
    "student": "home",
    "teacher": "home",
    "administrator": "home",
    "parent": "home",
    "manager": "home",
    "employee": "home",
}


@login_required
@require_POST
def select_role(request, role_slug):
    """
    POST-only role selection view.
    
    Query params:
        persist: If '1', saves to database (user.active_role)
                 Otherwise, stores in session only (ephemeral)
    
    Security:
        - Requires authentication
        - POST only (prevents CSRF, accidental switches)
        - Verifies user actually has the role
    """
    user = request.user
    role = get_object_or_404(Role, slug__iexact=role_slug)
    
    # Verify user has this role
    if not user.roles.filter(pk=role.pk).exists():
        messages.error(request, "You don't have access to this role.")
        return redirect("home")
    
    # Determine persistence method
    persist = request.POST.get("persist") == "1"
    
    if persist:
        # Save to database
        with transaction.atomic():
            user.active_role = role
            user.save(update_fields=["active_role"])
        messages.success(request, f"Active role permanently set to {role.name}")
    else:
        # Session-only (ephemeral)
        request.session["active_role_id"] = role.pk
        messages.success(request, f"Active role set to {role.name} for this session")
    
    # Redirect to role-specific page
    key = role.slug.lower()
    redirect_url = REDIRECT_MAP.get(key, "home")
    
    try:
        return redirect(reverse(redirect_url))
    except Exception:
        # Fallback if URL name doesn't exist
        return redirect("home")
