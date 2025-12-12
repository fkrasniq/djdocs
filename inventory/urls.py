from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('devices/', views.DeviceListView.as_view(), name='device-list'),
    path('devices/<slug:slug>/', views.DeviceDetailView.as_view(), name='device-detail'),
    path('api/topology/', views.network_topology_json, name='network-topology-json'),
    path('api/topology/<slug:slug>/', views.device_topology_json, name='device-topology-json'),
]
