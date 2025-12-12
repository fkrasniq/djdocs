from django.test import TestCase
from .models import Device, Interface, Connection


class DeviceModelTest(TestCase):
    def setUp(self):
        self.device = Device.objects.create(
            name='TestServer',
            device_type='server',
            ip_address='192.168.1.10'
        )
    
    def test_device_creation(self):
        self.assertTrue(self.device.id)
        self.assertEqual(self.device.name, 'TestServer')
        self.assertTrue(self.device.is_active)
    
    def test_device_slug_generation(self):
        self.assertEqual(self.device.slug, 'testserver')
    
    def test_device_absolute_url(self):
        self.assertIn('testserver', self.device.get_absolute_url())


class InterfaceModelTest(TestCase):
    def setUp(self):
        self.device = Device.objects.create(
            name='TestSwitch',
            device_type='switch'
        )
        self.interface = Interface.objects.create(
            device=self.device,
            name='Gi0/0/1',
            interface_type='ethernet',
            ip_address='10.0.0.1'
        )
    
    def test_interface_creation(self):
        self.assertEqual(self.interface.device, self.device)
        self.assertEqual(self.interface.name, 'Gi0/0/1')


class ConnectionModelTest(TestCase):
    def setUp(self):
        self.device1 = Device.objects.create(name='Device1', device_type='server')
        self.device2 = Device.objects.create(name='Device2', device_type='switch')
        self.iface1 = Interface.objects.create(
            device=self.device1,
            name='eth0',
            interface_type='ethernet'
        )
        self.iface2 = Interface.objects.create(
            device=self.device2,
            name='Gi0/0/1',
            interface_type='ethernet'
        )
        self.connection = Connection.objects.create(
            source_interface=self.iface1,
            destination_interface=self.iface2,
            connection_type='physical'
        )
    
    def test_connection_creation(self):
        self.assertEqual(self.connection.source_interface, self.iface1)
        self.assertEqual(self.connection.destination_interface, self.iface2)
