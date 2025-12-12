from django.contrib import admin
from .models import Diagram


@admin.register(Diagram)
class DiagramAdmin(admin.ModelAdmin):
    list_display = ['name', 'diagram_type', 'is_published']
    list_filter = ['diagram_type', 'is_published']
    search_fields = ['name', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    filter_horizontal = ['devices']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'diagram_type')
        }),
        ('Diagram Content', {
            'fields': ('mermaid_code',)
        }),
        ('Devices', {
            'fields': ('devices',)
        }),
        ('Status', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )
