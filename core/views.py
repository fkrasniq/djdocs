from django.shortcuts import render
from django.views.generic import TemplateView
from inventory.models import Device
from visualization.models import Diagram
from blog.models import Article
from django.db.models import Count


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics
        context['total_devices'] = Device.objects.filter(is_active=True).count()
        context['total_interfaces'] = Device.objects.aggregate(
            count=Count('interfaces')
        )['count'] or 0
        context['total_diagrams'] = Diagram.objects.filter(is_published=True).count()
        context['total_articles'] = Article.objects.filter(is_published=True).count()
        
        # Get recent items for dashboard
        context['recent_devices'] = Device.objects.filter(is_active=True).order_by('-updated_at')[:5]
        context['recent_diagrams'] = Diagram.objects.filter(is_published=True).order_by('-updated_at')[:5]
        context['recent_articles'] = Article.objects.filter(is_published=True).order_by('-created_at')[:5]
        
        # Get device type distribution
        context['device_types'] = Device.objects.values('device_type').annotate(count=Count('id')).order_by('-count')
        
        return context
