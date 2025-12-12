from django.test import TestCase
from inventory.models import Device
from .models import Diagram


class DiagramModelTest(TestCase):
    def setUp(self):
        self.device = Device.objects.create(name='TestDevice', device_type='server')
        self.diagram = Diagram.objects.create(
            name='TestDiagram',
            diagram_type='network'
        )
        self.diagram.devices.add(self.device)
    
    def test_diagram_creation(self):
        self.assertEqual(self.diagram.name, 'TestDiagram')
        self.assertIn(self.device, self.diagram.devices.all())
    
    def test_diagram_slug_generation(self):
        self.assertEqual(self.diagram.slug, 'testdiagram')
