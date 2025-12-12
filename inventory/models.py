from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator


class Device(models.Model):
    """Represents a network device (Server, Switch, Firewall, Printer, etc.)"""
    
    DEVICE_TYPES = [
        ('server', 'Server'),
        ('switch', 'Network Switch'),
        ('firewall', 'Firewall'),
        ('router', 'Router'),
        ('printer', 'Printer'),
        ('workstation', 'Workstation'),
        ('storage', 'Storage'),
        ('other', 'Other'),
    ]
    
    OS_TYPES = [
        ('windows', 'Windows'),
        ('linux', 'Linux'),
        ('macos', 'macOS'),
        ('cisco', 'Cisco IOS'),
        ('junos', 'Juniper JunOS'),
        ('paloalto', 'Palo Alto Networks'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    os_type = models.CharField(max_length=50, choices=OS_TYPES, blank=True, null=True)
    
    # Network details
    ip_address = models.GenericIPAddressField(unique=True, blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    
    # Physical details
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    rack_id = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 'Rack-01'")
    rack_unit_start = models.PositiveIntegerField(blank=True, null=True, help_text="Starting U position (1-based)")
    rack_unit_height = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], help_text="Number of U units occupied")
    
    # Status and metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['device_type']),
            models.Index(fields=['ip_address']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('inventory:device-detail', kwargs={'slug': self.slug})


class Interface(models.Model):
    """Represents a network interface (Ethernet, WLAN, etc.) on a Device"""
    
    INTERFACE_TYPES = [
        ('ethernet', 'Ethernet'),
        ('wifi', 'WiFi/WLAN'),
        ('serial', 'Serial'),
        ('usb', 'USB'),
        ('optical', 'Optical Fiber'),
        ('other', 'Other'),
    ]
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='interfaces')
    name = models.CharField(max_length=255, help_text="e.g., 'eth0', 'Gi0/0/1'")
    interface_type = models.CharField(max_length=50, choices=INTERFACE_TYPES)
    
    # Network settings
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    vlan_id = models.PositiveIntegerField(blank=True, null=True)
    
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['device', 'name']
        unique_together = [['device', 'name']]
        indexes = [
            models.Index(fields=['device']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"{self.device.name} - {self.name}"


class Connection(models.Model):
    """Represents a connection between two interfaces"""
    
    source_interface = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        related_name='outgoing_connections'
    )
    destination_interface = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        related_name='incoming_connections'
    )
    
    connection_type = models.CharField(
        max_length=50,
        choices=[
            ('physical', 'Physical Cable'),
            ('logical', 'Logical Link'),
            ('vlan', 'VLAN Trunk'),
            ('wireless', 'Wireless'),
        ],
        default='physical'
    )
    
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['source_interface', 'destination_interface']
        unique_together = [['source_interface', 'destination_interface']]
        indexes = [
            models.Index(fields=['source_interface']),
            models.Index(fields=['destination_interface']),
        ]
    
    def __str__(self):
        return f"{self.source_interface} → {self.destination_interface}"
