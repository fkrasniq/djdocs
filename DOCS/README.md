# Asset-Linked Knowledge Base: Visual Infrastructure & Asset Manager

A Django-based system combining a Configuration Management Database (CMDB) with a Wiki, featuring data-driven network diagrams and visualizations that update automatically when the database changes.

## Project Overview

This project implements a comprehensive solution for managing IT infrastructure and documentation with interactive visualizations including:

- **Network Topology Maps** (Vis.js) - Interactive, physics-based network visualization
- **Flowcharts & Process Diagrams** (Mermaid.js) - Code-based diagrams for processes and flows
- **Data Dashboards** (Chart.js) - Analytics and license capacity tracking
- **Rack Elevations** - Dynamic HTML/CSS representations of server racks

## Architecture

### 1. Inventory App (`inventory/`)
Manages the physical IT infrastructure layer.

**Models:**
- **Device**: Represents servers, switches, firewalls, printers, etc.
  - Fields: name, device_type, OS type, IP address, MAC address, serial number, location
  - Rack support: `rack_id`, `rack_unit_start`, `rack_unit_height`
  
- **Interface**: Network interfaces on devices (Ethernet, WLAN, Serial, etc.)
  - Fields: name, interface_type, IP address, MAC address, VLAN ID
  - Relations: ForeignKey to Device

- **Connection**: Links between two interfaces
  - Fields: connection_type (physical/logical/VLAN/wireless)
  - Relations: ForeignKey to source and destination interfaces

**Views:**
- `DeviceListView`: Paginated list of all devices with filtering
- `DeviceDetailView`: Detailed device view with interfaces and network topology
- JSON endpoints for topology data (used by Vis.js)

**Admin Interface:**
- Full CRUD for Devices, Interfaces, Connections
- Inline interface creation on Device admin page
- Filtering and search capabilities

### 2. Visualization App (`visualization/`)
Manages diagram definitions and groupings.

**Models:**
- **Diagram**: Container for grouping devices and storing visualization definitions
  - Fields: name, diagram_type (network/rack/process/custom)
  - Mermaid code support for flowcharts
  - M2M relationship with Devices

**Views:**
- `DiagramListView`: List all published diagrams
- `DiagramDetailView`: Display diagram with associated devices

**Admin Interface:**
- Create/edit diagrams
- Associate devices with diagrams
- Embed Mermaid code

### 3. Blog App (`blog/`)
Enhanced documentation system with diagram embedding.

**Models:**
- **Article**: Rich text documentation
  - Fields: title, content (markdown/HTML), description
  - Relations: ForeignKey to User (author)
  
- **ArticleEmbed**: Embeds diagrams, devices, or Mermaid code within articles
  - Supports: Diagrams, Devices, Mermaid code, Charts
  - Order-based positioning
  - Optional caption and width settings

**Views:**
- `ArticleListView`: Published articles
- `ArticleDetailView`: Full article with embedded visualizations

**Admin Interface:**
- Article creation with inline embeds
- Multiple embed types

### 4. Accounts App (`accounts/`)
User and role management (already implemented).

## Visualization Libraries

### Frontend Libraries
All integrated via CDN in `templates/base.html`:

1. **Bootstrap 5**: Responsive UI framework
2. **FontAwesome 6.4**: Icon library for device types
3. **Mermaid.js**: Flowcharts and process diagrams
   ```javascript
   // Example: Simple network flow
   graph TD;
       Firewall-->Switch01;
       Switch01-->ServerA;
       Switch01-->ServerB;
   ```

4. **Vis.js**: Interactive network topology visualization
   - Physics-based node positioning
   - Click handlers for navigation
   - Dynamic data loading from JSON endpoints

5. **Chart.js**: Data visualization and analytics
   - Pie charts, bar charts, line graphs
   - Real-time data updates

## Usage Examples

### Adding a Device
1. Navigate to Django admin (`/admin/`)
2. Click "Devices" in Inventory section
3. Fill in device details (name, type, OS, IP address)
4. Add interfaces inline
5. Save

### Creating a Network Diagram
1. Go to Admin → Visualization → Diagrams
2. Set diagram type to "Network Topology"
3. Associate devices
4. (Optional) Add Mermaid code for flowchart
5. Publish

### Creating Documentation with Diagrams
1. Go to Admin → Blog → Articles
2. Write article content
3. Add embeds (inline) for diagrams/devices/Mermaid code
4. Publish

### Viewing Network Topology
1. Visit `/inventory/devices/<device-slug>/`
2. Network diagram at bottom shows connected devices
3. Click nodes to view details
4. Interactive: drag to reposition, scroll to zoom

## Database Models Overview

```
Device (1) ←→ (M) Interface
                   ↓
            Connection
            (Interface ←→ Interface)

Device (M) ←→ (M) Diagram

Article (1) ←→ (M) ArticleEmbed
                      ↓
                 Diagram / Device / Mermaid Code
```

## File Structure

```
djdocs/
├── inventory/
│   ├── models.py          # Device, Interface, Connection
│   ├── views.py           # List/Detail views + JSON endpoints
│   ├── admin.py           # Admin configuration
│   ├── urls.py            # URL routing
│   ├── migrations/         # Database migrations
│   └── templates/
│       ├── device_list.html
│       └── device_detail.html
│
├── visualization/
│   ├── models.py          # Diagram model
│   ├── views.py           # Diagram views
│   ├── admin.py           # Admin config
│   ├── urls.py            # URL routing
│   ├── migrations/
│   └── templates/
│       ├── diagram_list.html
│       └── diagram_detail.html
│
├── blog/
│   ├── models.py          # Article, ArticleEmbed
│   ├── views.py           # Blog views
│   ├── admin.py           # Admin config
│   ├── urls.py            # URL routing
│   ├── migrations/
│   └── templates/
│       ├── article_list.html
│       └── article_detail.html
│
├── accounts/              # User management (existing)
├── tasks/                 # Task tracking (existing)
│
├── templates/
│   ├── base.html          # Base template with libraries
│   ├── inventory/
│   ├── visualization/
│   └── blog/
│
├── static/                # Static files (CSS, JS, images)
├── manage.py
├── db.sqlite3             # Development database
└── djdocs/
    ├── settings.py        # Django settings
    ├── urls.py            # Main URL config
    └── wsgi.py
```

## Running the Application

### 1. Activate Virtual Environment
```bash
# Windows PowerShell
c:/dev/testing/autoc/djdocs/test_env/Scripts/Activate.ps1

# Windows Command Prompt
c:\dev\testing\autoc\djdocs\test_env\Scripts\activate.bat
```

### 2. Run Migrations (if needed)
```bash
python manage.py migrate
```

### 3. Create Superuser (first time only)
```bash
python manage.py createsuperuser
```

### 4. Start Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- Main site: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Devices: `http://127.0.0.1:8000/inventory/devices/`
- Diagrams: `http://127.0.0.1:8000/visualization/diagrams/`
- Articles: `http://127.0.0.1:8000/blog/articles/`

## Key Features Implemented

✅ **Device Inventory Management**
- Full CRUD for devices and interfaces
- Multiple device types and OS support
- Network connection tracking
- Rack elevation support with U-position tracking

✅ **Network Visualization**
- Interactive Vis.js topology maps
- Device grouping via Diagrams
- Dynamic JSON endpoints
- Click handlers for navigation

✅ **Documentation System**
- Rich text articles with markdown support
- Embedded diagrams and device references
- Ordered embeds within articles
- Published/draft status

✅ **Admin Interface**
- Inline device interface creation
- Device association with diagrams
- Article embed management
- Search and filtering

✅ **Visualization Libraries**
- Mermaid.js for flowcharts
- Vis.js for network topology
- Chart.js ready for analytics
- FontAwesome icons
- Bootstrap 5 responsive design

## Future Enhancements

1. **Rack Visualization**: CSS Grid-based rack elevation rendering
2. **API Integration**: Real-time data from monitoring tools (Nagios, Prometheus)
3. **Advanced Charts**: License tracking, capacity planning dashboards
4. **Cytoscape.js**: Alternative network visualization with hierarchical layouts
5. **API Endpoints**: RESTful API for external integrations
6. **Full-Text Search**: Elasticsearch integration for device/article search
7. **Audit Logging**: Track changes to devices and diagrams
8. **Multi-tenancy**: Support multiple organizations/sites

## Technology Stack

- **Backend**: Django 6.0
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **Visualization**: Mermaid.js, Vis.js, Chart.js
- **Icons**: FontAwesome 6.4
- **CSS/JS CDN**: jsDelivr

## Notes

- The project uses SQLite for development. For production, use PostgreSQL or MySQL.
- All visualization libraries are loaded from CDN for simplicity.
- Static files should be collected before production deployment: `python manage.py collectstatic`
- The project includes role-based access control via the Accounts app.
- Device models support rack positioning for future rack elevation visualization.

## Support & Customization

To extend this project:

1. **Add Device Types**: Edit `Device.DEVICE_TYPES` in `inventory/models.py`
2. **Create Custom Diagrams**: Add new `diagram_type` choices to `Diagram` model
3. **Custom Visualizations**: Create new views and templates following the existing patterns
4. **API Endpoints**: Add ViewSets using Django REST Framework
5. **Real-time Updates**: Integrate Django Channels for WebSocket support

---

**Project Status**: ✅ Core implementation complete with all major features operational.
**Last Updated**: December 2025
