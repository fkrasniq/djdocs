from django.db import models
from django.utils.text import slugify
from inventory.models import Device


class Diagram(models.Model):
    """Container for grouping specific devices in a visualization"""
    
    DIAGRAM_TYPES = [
        ('network', 'Network Topology'),
        ('rack', 'Rack Elevation'),
        ('process', 'Process Flow'),
        ('custom', 'Custom'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    diagram_type = models.CharField(max_length=50, choices=DIAGRAM_TYPES)
    
    # Mermaid diagram code (for flowcharts/process diagrams)
    mermaid_code = models.TextField(
        blank=True,
        null=True,
        help_text="Mermaid.js diagram code for flowcharts, etc."
    )
    
    # Associated devices
    devices = models.ManyToManyField(
        Device,
        blank=True,
        related_name='diagrams'
    )
    
    # Display settings
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['diagram_type']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('visualization:diagram-detail', kwargs={'slug': self.slug})
