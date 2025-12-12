from django.contrib import admin
from .models import Device, Interface, Connection


class InterfaceInline(admin.TabularInline):
    model = Interface
    extra = 1
    fields = ['name', 'interface_type', 'ip_address', 'mac_address', 'is_active']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'device_type', 'os_type', 'ip_address', 'location', 'is_active']
    list_filter = ['device_type', 'os_type', 'is_active', 'location']
    search_fields = ['name', 'ip_address', 'serial_number']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    inlines = [InterfaceInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'device_type', 'os_type')
        }),
        ('Network', {
            'fields': ('ip_address', 'mac_address')
        }),
        ('Physical', {
            'fields': ('serial_number', 'location', 'rack_id', 'rack_unit_start', 'rack_unit_height')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'device', 'interface_type', 'ip_address', 'is_active']
    list_filter = ['device', 'interface_type', 'is_active']
    search_fields = ['name', 'ip_address', 'device__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['source_interface', 'destination_interface', 'connection_type', 'is_active']
    list_filter = ['connection_type', 'is_active']
    search_fields = ['source_interface__name', 'destination_interface__name', 'description']
    readonly_fields = ['created_at', 'updated_at']
