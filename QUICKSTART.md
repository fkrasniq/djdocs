# Quick Start Guide

## 1. Activate Virtual Environment

```powershell
# Windows PowerShell
c:/dev/testing/autoc/djdocs/test_env/Scripts/Activate.ps1

# Or Windows Command Prompt
c:\dev\testing\autoc\djdocs\test_env\Scripts\activate.bat
```

## 2. Run the Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

## 3. Access the Application

### Admin Dashboard
- URL: `http://127.0.0.1:8000/admin/`
- Create your first user here
- Add devices, interfaces, diagrams, and articles

### Main Views
- **Devices**: `http://127.0.0.1:8000/inventory/devices/`
- **Diagrams**: `http://127.0.0.1:8000/visualization/diagrams/`
- **Articles**: `http://127.0.0.1:8000/blog/articles/`

## 4. Creating Test Data

### Option A: Via Admin Interface
1. Go to `/admin/`
2. Click on "Devices" under "Inventory"
3. Click "Add Device"
4. Fill in the form:
   - **Name**: e.g., "Web-Server-01"
   - **Device Type**: Select "Server"
   - **OS Type**: Select "Linux"
   - **IP Address**: e.g., "192.168.1.100"
   - **Location**: e.g., "Data Center"
5. Click "Save"
6. Add interfaces by scrolling down to "Interfaces" and clicking "Add Another Interface"
   - **Name**: e.g., "eth0"
   - **Interface Type**: Select "Ethernet"
   - **IP Address**: e.g., "192.168.1.100"
7. Click "Save"

### Option B: Python Shell
```bash
python manage.py shell

# Then in the shell:
from inventory.models import Device, Interface

# Create a device
device = Device.objects.create(
    name='Test-Server-01',
    device_type='server',
    os_type='linux',
    ip_address='192.168.1.50'
)

# Create an interface
interface = Interface.objects.create(
    device=device,
    name='eth0',
    interface_type='ethernet',
    ip_address='192.168.1.50'
)

print(f"Created {device.name} with interface {interface.name}")
```

## 5. Creating Network Connections

In the admin dashboard:
1. Go to **Connections** under **Inventory**
2. Click "Add Connection"
3. Select:
   - **Source Interface**: First device's interface
   - **Destination Interface**: Second device's interface
   - **Connection Type**: Physical, Logical, VLAN, or Wireless
4. Click "Save"

## 6. Creating Diagrams

1. Go to Admin → **Diagrams** under **Visualization**
2. Click "Add Diagram"
3. Fill in:
   - **Name**: e.g., "Data Center Network"
   - **Diagram Type**: Network Topology, Rack Elevation, Process Flow, or Custom
   - **Devices**: Select devices to include (use Ctrl+Click for multiple)
   - **Mermaid Code**: (Optional) Add flowchart code like:
     ```
     graph TD;
         A[Firewall] --> B[Switch];
         B --> C[Server];
     ```
4. Check "Published" to make it visible
5. Click "Save"

## 7. Creating Articles with Embedded Diagrams

1. Go to Admin → **Articles** under **Blog**
2. Click "Add Article"
3. Fill in:
   - **Title**: e.g., "Network Architecture Guide"
   - **Content**: Write your article (supports HTML)
   - **Author**: Select yourself
   - **Is Published**: Check to make visible
4. Scroll down to "Embeds" and click "Add another Embed"
5. Select:
   - **Embed Type**: Diagram, Device, Mermaid, or Chart
   - **Diagram**: (if type=Diagram) Select which diagram to embed
   - **Device**: (if type=Device) Select which device to display
   - **Order**: Position in article (0 = first)
   - **Caption**: Description of the embed
6. Click "Save"

## 8. Viewing Network Topology

1. Visit `/inventory/devices/` to see all devices
2. Click on a device to view its detail page
3. Scroll down to see the interactive network topology
   - **Click**: Select a device
   - **Drag**: Move device nodes around
   - **Scroll**: Zoom in/out
4. Connected devices are shown automatically

## 9. Viewing Diagrams

1. Visit `/visualization/diagrams/` to see all diagrams
2. Click on a diagram to view it
3. Connected devices are listed below

## 10. Reading Documentation

1. Visit `/blog/articles/` to see published articles
2. Click on an article to read it
3. Embedded diagrams and device information appear inline

## Troubleshooting

### Port Already in Use
If port 8000 is busy, use:
```bash
python manage.py runserver 8001
```

### Database Issues
Reset the database:
```bash
python manage.py flush --noinput
python manage.py migrate
```

### Missing Static Files
Collect static files:
```bash
python manage.py collectstatic --noinput
```

### Import Errors
Ensure virtual environment is activated:
```bash
c:/dev/testing/autoc/djdocs/test_env/Scripts/Activate.ps1
```

## Key URLs Reference

| Feature | URL |
|---------|-----|
| Admin Dashboard | `/admin/` |
| All Devices | `/inventory/devices/` |
| Device Detail | `/inventory/devices/<slug>/` |
| Network Topology API | `/inventory/api/topology/` |
| Device Topology API | `/inventory/api/topology/<slug>/` |
| All Diagrams | `/visualization/diagrams/` |
| Diagram Detail | `/visualization/diagrams/<slug>/` |
| All Articles | `/blog/articles/` |
| Article Detail | `/blog/articles/<slug>/` |

## Next Steps

- Customize device types and OS types in `inventory/models.py`
- Add custom CSS styles in `templates/base.html`
- Create API endpoints for external integrations
- Set up automatic data collection from monitoring tools
- Configure email notifications for device changes
- Implement user roles and permissions

---

For more details, see [README.md](README.md)
