"""
Sample data loading script for testing the Asset Manager
Run with: python manage.py shell < load_sample_data.py
"""

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

storage = Device.objects.create(
    name='Storage-Array-01',
    device_type='storage',
    ip_address='192.168.1.200',
    location='Data Center - Rack 04',
    rack_id='Rack-04',
    rack_unit_start=10,
    rack_unit_height=4,
    description='SAN storage for backup and archival'
)
devices.append(storage)
print(f"✓ Created: {storage.name}")

workstation = Device.objects.create(
    name='Admin-Workstation-01',
    device_type='workstation',
    os_type='windows',
    ip_address='192.168.2.50',
    location='Office Building - IT Dept',
    description='Admin workstation for system management'
)
devices.append(workstation)
print(f"✓ Created: {workstation.name}")

# Create interfaces
print("\nCreating network interfaces...")
ifaces = []

# Firewall interfaces
fw_eth0 = Interface.objects.create(
    device=firewall,
    name='eth0',
    interface_type='ethernet',
    ip_address='192.168.1.1',
    description='WAN Interface'
)
ifaces.append(fw_eth0)

fw_eth1 = Interface.objects.create(
    device=firewall,
    name='eth1',
    interface_type='ethernet',
    ip_address='192.168.1.2',
    description='LAN Interface'
)
ifaces.append(fw_eth1)
print(f"✓ Created interfaces for {firewall.name}")

# Switch 1 interfaces
sw1_gi00 = Interface.objects.create(
    device=switch1,
    name='Gi0/0/1',
    interface_type='ethernet',
    description='Uplink to Firewall'
)
ifaces.append(sw1_gi00)

sw1_gi01 = Interface.objects.create(
    device=switch1,
    name='Gi0/0/2',
    interface_type='ethernet',
    description='Uplink to Access Switch'
)
ifaces.append(sw1_gi01)

sw1_gi02 = Interface.objects.create(
    device=switch1,
    name='Gi0/0/3',
    interface_type='ethernet',
    description='Server Port 1'
)
ifaces.append(sw1_gi02)

sw1_gi03 = Interface.objects.create(
    device=switch1,
    name='Gi0/0/4',
    interface_type='ethernet',
    description='Server Port 2'
)
ifaces.append(sw1_gi03)
print(f"✓ Created interfaces for {switch1.name}")

# Access Switch interfaces
sw2_gi00 = Interface.objects.create(
    device=switch2,
    name='Gi0/0/1',
    interface_type='ethernet',
    description='Uplink to Core Switch'
)
ifaces.append(sw2_gi00)

sw2_gi01 = Interface.objects.create(
    device=switch2,
    name='Gi0/0/2',
    interface_type='ethernet',
    description='Workstation Port'
)
ifaces.append(sw2_gi01)
print(f"✓ Created interfaces for {switch2.name}")

# Server interfaces
srv1_eth0 = Interface.objects.create(
    device=server1,
    name='eth0',
    interface_type='ethernet',
    ip_address='192.168.1.100',
    description='Primary Network'
)
ifaces.append(srv1_eth0)

srv2_eth0 = Interface.objects.create(
    device=server2,
    name='eth0',
    interface_type='ethernet',
    ip_address='192.168.1.101',
    description='Primary Network'
)
ifaces.append(srv2_eth0)
print(f"✓ Created interfaces for servers")

# Storage interface
stor_eth0 = Interface.objects.create(
    device=storage,
    name='eth0',
    interface_type='ethernet',
    ip_address='192.168.1.200',
    description='Storage Network'
)
ifaces.append(stor_eth0)
print(f"✓ Created interface for {storage.name}")

# Workstation interface
ws_eth0 = Interface.objects.create(
    device=workstation,
    name='eth0',
    interface_type='ethernet',
    ip_address='192.168.2.50',
    description='Network'
)
ifaces.append(ws_eth0)
print(f"✓ Created interface for {workstation.name}")

# Create connections
print("\nCreating network connections...")

# Firewall to Core Switch
Connection.objects.create(
    source_interface=fw_eth1,
    destination_interface=sw1_gi00,
    connection_type='physical',
    description='WAN Connection'
)
print(f"✓ Connected {firewall.name} → {switch1.name}")

# Core Switch to Access Switch
Connection.objects.create(
    source_interface=sw1_gi01,
    destination_interface=sw2_gi00,
    connection_type='physical',
    description='Core to Access uplink'
)
print(f"✓ Connected {switch1.name} → {switch2.name}")

# Core Switch to Servers
Connection.objects.create(
    source_interface=sw1_gi02,
    destination_interface=srv1_eth0,
    connection_type='physical',
    description='Web Server connection'
)
print(f"✓ Connected {switch1.name} → {server1.name}")

Connection.objects.create(
    source_interface=sw1_gi03,
    destination_interface=srv2_eth0,
    connection_type='physical',
    description='Database Server connection'
)
print(f"✓ Connected {switch1.name} → {server2.name}")

# Access Switch to Workstation
Connection.objects.create(
    source_interface=sw2_gi01,
    destination_interface=ws_eth0,
    connection_type='physical',
    description='Admin workstation'
)
print(f"✓ Connected {switch2.name} → {workstation.name}")

# Create diagrams
print("\nCreating sample diagrams...")

diagram1 = Diagram.objects.create(
    name='Data Center Network',
    diagram_type='network',
    description='Core data center infrastructure',
    is_published=True,
    mermaid_code='''graph TD
    Firewall["🔥 Firewall<br/>192.168.1.1"]
    CoreSwitch["🔀 Core Switch<br/>192.168.1.10"]
    WebServer["🖥️ Web Server<br/>192.168.1.100"]
    DBServer["🗄️ DB Server<br/>192.168.1.101"]
    Storage["💾 Storage<br/>192.168.1.200"]
    
    Firewall -->|WAN| CoreSwitch
    CoreSwitch -->|eth0/3| WebServer
    CoreSwitch -->|eth0/4| DBServer
    CoreSwitch -->|eth0/5| Storage
    
    style Firewall fill:#ff6b6b
    style CoreSwitch fill:#4ecdc4
    style WebServer fill:#45b7d1
    style DBServer fill:#96ceb4
    style Storage fill:#ffeaa7'''
)
diagram1.devices.set([firewall, switch1, server1, server2, storage])
print(f"✓ Created diagram: {diagram1.name}")

diagram2 = Diagram.objects.create(
    name='Office Network',
    diagram_type='network',
    description='Office building network topology',
    is_published=True
)
diagram2.devices.set([switch2, workstation])
print(f"✓ Created diagram: {diagram2.name}")

# Create articles
print("\nCreating sample articles...")

article1 = Article.objects.create(
    title='Network Infrastructure Overview',
    slug='network-infrastructure-overview',
    content='''
    <h2>Overview</h2>
    <p>This document outlines the current network infrastructure setup.</p>
    
    <h3>Data Center Core</h3>
    <p>Our data center is built on a redundant architecture with core firewalls, 
    switches, and servers interconnected for maximum reliability.</p>
    
    <h3>Key Components</h3>
    <ul>
        <li>Core firewall for WAN connection</li>
        <li>Core switch for intra-datacenter routing</li>
        <li>Web and database servers</li>
        <li>Storage array for backup</li>
    </ul>
    ''',
    description='Technical overview of the entire network infrastructure',
    author=admin_user,
    is_published=True
)
print(f"✓ Created article: {article1.title}")

# Create embeds
ArticleEmbed.objects.create(
    article=article1,
    embed_type='diagram',
    diagram=diagram1,
    order=1,
    caption='Data Center Network Topology'
)
print(f"  ✓ Added diagram embed to article")

ArticleEmbed.objects.create(
    article=article1,
    embed_type='device',
    device=server1,
    order=2,
    caption='Web Server Details'
)
print(f"  ✓ Added device embed to article")

ArticleEmbed.objects.create(
    article=article1,
    embed_type='mermaid',
    mermaid_code='''graph LR
    A[User] -->|HTTPS| B[Web Server]
    B -->|Query| C[DB Server]
    C -->|Store| D[Storage]
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9''',
    order=3,
    caption='Data Flow Diagram'
)
print(f"  ✓ Added Mermaid embed to article")

print("\n" + "="*50)
print("✅ Sample data loaded successfully!")
print("="*50)
print(f"\nSummary:")
print(f"  Devices: {Device.objects.count()}")
print(f"  Interfaces: {Interface.objects.count()}")
print(f"  Connections: {Connection.objects.count()}")
print(f"  Diagrams: {Diagram.objects.count()}")
print(f"  Articles: {Article.objects.count()}")
print(f"\nNext steps:")
print(f"  1. Start the server: python manage.py runserver")
print(f"  2. Visit http://localhost:8000/admin/ (use admin@example.com / admin123)")
print(f"  3. Browse devices at http://localhost:8000/inventory/devices/")
print(f"  4. View diagrams at http://localhost:8000/visualization/diagrams/")
print(f"  5. Read articles at http://localhost:8000/blog/articles/")
