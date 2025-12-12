from django.urls import path
from . import views

app_name = 'visualization'

urlpatterns = [
    path('diagrams/', views.DiagramListView.as_view(), name='diagram-list'),
    path('diagrams/<slug:slug>/', views.DiagramDetailView.as_view(), name='diagram-detail'),
]
