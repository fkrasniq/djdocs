#!/usr/bin/env python
"""
Django management command to load sample data.
Run with: python manage.py shell < load_sample_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djdocs.settings')
django.setup()

from inventory.models import Device, Interface, Connection
from visualization.models import Diagram
from accounts.models import User
from blog.models import Article, ArticleEmbed

# Create sample users
print("Creating sample users...")
try:
    admin_user = User.objects.get(email='admin@example.com')
except User.DoesNotExist:
    admin_user = User.objects.create_superuser(
        email='admin@example.com',
        password='admin123'
    )
    print(f"✓ Created admin user: {admin_user.email}")

# Create sample devices
print("\nCreating sample devices...")
devices = []

firewall = Device.objects.create(
    name='Core-Firewall-01',
    device_type='firewall',
    os_type='paloalto',
    ip_address='192.168.1.1',
    location='Data Center - Rack 01',
    rack_id='Rack-01',
    rack_unit_start=40,
    rack_unit_height=2
)
devices.append(firewall)
print(f"✓ Created: {firewall.name}")

switch1 = Device.objects.create(
    name='Core-Switch-01',
    device_type='switch',
    os_type='cisco',
    ip_address='192.168.1.10',
    location='Data Center - Rack 02',
    rack_id='Rack-02',
    rack_unit_start=38,
    rack_unit_height=2
)
devices.append(switch1)
print(f"✓ Created: {switch1.name}")

switch2 = Device.objects.create(
    name='Access-Switch-01',
    device_type='switch',
    os_type='cisco',
    ip_address='192.168.2.10',
    location='Office Building - Floor 2'
)
devices.append(switch2)
print(f"✓ Created: {switch2.name}")

server1 = Device.objects.create(
    name='Web-Server-01',
    device_type='server',
    os_type='linux',
    ip_address='192.168.1.100',
    location='Data Center - Rack 03',
    rack_id='Rack-03',
    rack_unit_start=20,
    rack_unit_height=2,
    description='Primary web server hosting main applications'
)
devices.append(server1)
print(f"✓ Created: {server1.name}")

server2 = Device.objects.create(
    name='DB-Server-01',
    device_type='server',
    os_type='linux',
    ip_address='192.168.1.101',
    location='Data Center - Rack 03',
    rack_id='Rack-03',
    rack_unit_start=18,
    rack_unit_height=2,
    description='Database server for production data'
)
devices.append(server2)
print(f"✓ Created: {server2.name}")

print("\n" + "="*50)
print("✅ Sample devices created successfully!")
print("="*50)
print(f"\nNext steps:")
print(f"  1. Start the server: python manage.py runserver")
print(f"  2. Visit http://localhost:8000/inventory/devices/")
print(f"  3. View device details at http://localhost:8000/inventory/devices/<device-slug>/")
