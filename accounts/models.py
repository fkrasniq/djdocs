from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Permission,
)
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from PIL import Image


class Role(models.Model):
    """Role model for user role-based access control."""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    class Meta:
        indexes = [models.Index(fields=["slug"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # Role-based access control
    roles = models.ManyToManyField(Role, blank=True, related_name='users')
    active_role = models.ForeignKey(
        Role, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="active_users"
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    
    def has_role(self, role_identifier):
        """Check if user has a specific role by slug or name."""
        return self.roles.filter(
            models.Q(slug__iexact=role_identifier) | 
            models.Q(name__iexact=role_identifier)
        ).exists()
    
    def set_active_role(self, role=None, *, persist=True):
        """
        Set the active role for the user.
        
        Args:
            role: Role instance, slug, or name
            persist: If True, save to DB. If False, session-only (handled in view)
        
        Returns:
            Role instance that was set
        
        Raises:
            ValueError: If role not found or not assigned to user
        """
        if isinstance(role, Role):
            r = role
        else:
            r = self.roles.filter(
                models.Q(slug__iexact=role) | 
                models.Q(name__iexact=role)
            ).first()
        
        if not r:
            raise ValueError("Role not found or not assigned to user")
        
        self.active_role = r
        if persist:
            self.save(update_fields=["active_role"])
        return r


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        verbose_name="user",
        related_name="profile",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(
        default="profile_img/default.jpg",
        upload_to="media/profile_img",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.user.name:
            return f"{self.user.name}'s profile"
        return f"{self.user.email}'s profile"

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
