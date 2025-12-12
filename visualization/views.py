from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Diagram


class DiagramListView(ListView):
    model = Diagram
    template_name = 'visualization/diagram_list.html'
    context_object_name = 'diagrams'
    paginate_by = 50
    
    def get_queryset(self):
        return Diagram.objects.filter(is_published=True)


class DiagramDetailView(DetailView):
    model = Diagram
    template_name = 'visualization/diagram_detail.html'
    context_object_name = 'diagram'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Diagram.objects.filter(is_published=True)
