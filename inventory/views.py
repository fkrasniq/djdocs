from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Device, Interface, Connection
import json


class DeviceListView(ListView):
    model = Device
    template_name = 'inventory/device_list.html'
    context_object_name = 'devices'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = Device.objects.all()
        device_type = self.request.GET.get('type')
        if device_type:
            queryset = queryset.filter(device_type=device_type)
        return queryset


class DeviceDetailView(DetailView):
    model = Device
    template_name = 'inventory/device_detail.html'
    context_object_name = 'device'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.object
        context['interfaces'] = device.interfaces.all()
        context['outgoing_connections'] = device.interfaces.prefetch_related('outgoing_connections')
        context['incoming_connections'] = device.interfaces.prefetch_related('incoming_connections')
        return context


def device_topology_json(request, slug):
    """
    Returns JSON data for Vis.js network visualization.
    Includes the target device and all directly connected devices.
    """
    device = get_object_or_404(Device, slug=slug)
    
    # Collect all connected devices
    connected_device_ids = set([device.id])
    
    for interface in device.interfaces.all():
        # Outgoing connections
        for conn in interface.outgoing_connections.all():
            if conn.destination_interface.device_id not in connected_device_ids:
                connected_device_ids.add(conn.destination_interface.device_id)
        
        # Incoming connections
        for conn in interface.incoming_connections.all():
            if conn.source_interface.device_id not in connected_device_ids:
                connected_device_ids.add(conn.source_interface.device_id)
    
    # Get all relevant devices
    devices = Device.objects.filter(id__in=connected_device_ids)
    
    # Build nodes
    nodes = []
    for dev in devices:
        nodes.append({
            'id': str(dev.id),
            'label': dev.name,
            'title': f"{dev.name} ({dev.device_type})",
            'color': '#FF6B6B' if dev.id == device.id else '#4ECDC4',
            'font': {'size': 16 if dev.id == device.id else 14}
        })
    
    # Build edges
    edges = []
    edge_set = set()
    
    for interface in device.interfaces.all():
        for conn in interface.outgoing_connections.filter(is_active=True):
            src_id = str(conn.source_interface.device_id)
            dst_id = str(conn.destination_interface.device_id)
            edge_key = tuple(sorted([src_id, dst_id]))
            
            if edge_key not in edge_set:
                edges.append({
                    'from': src_id,
                    'to': dst_id,
                    'label': conn.connection_type,
                    'title': conn.description or ''
                })
                edge_set.add(edge_key)
    
    return JsonResponse({
        'nodes': nodes,
        'edges': edges
    })


def network_topology_json(request):
    """
    Returns JSON data for full network topology visualization.
    """
    devices = Device.objects.filter(is_active=True)
    connections = Connection.objects.filter(is_active=True)
    
    # Build nodes
    nodes = []
    for device in devices:
        nodes.append({
            'id': str(device.id),
            'label': device.name,
            'title': f"{device.name} ({device.device_type})",
            'color': '#4ECDC4'
        })
    
    # Build edges
    edges = []
    edge_set = set()
    
    for conn in connections:
        src_id = str(conn.source_interface.device_id)
        dst_id = str(conn.destination_interface.device_id)
        edge_key = tuple(sorted([src_id, dst_id]))
        
        if edge_key not in edge_set:
            edges.append({
                'from': src_id,
                'to': dst_id,
                'label': conn.connection_type,
            })
            edge_set.add(edge_key)
    
    return JsonResponse({
        'nodes': nodes,
        'edges': edges
    })
