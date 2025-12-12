# Generated migration for inventory app

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('device_type', models.CharField(choices=[('server', 'Server'), ('switch', 'Network Switch'), ('firewall', 'Firewall'), ('router', 'Router'), ('printer', 'Printer'), ('workstation', 'Workstation'), ('storage', 'Storage'), ('other', 'Other')], max_length=50)),
                ('os_type', models.CharField(blank=True, choices=[('windows', 'Windows'), ('linux', 'Linux'), ('macos', 'macOS'), ('cisco', 'Cisco IOS'), ('junos', 'Juniper JunOS'), ('paloalto', 'Palo Alto Networks'), ('other', 'Other')], max_length=50, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, unique=True)),
                ('mac_address', models.CharField(blank=True, max_length=17, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('rack_id', models.CharField(blank=True, max_length=50, null=True, help_text="e.g., 'Rack-01'")),
                ('rack_unit_start', models.PositiveIntegerField(blank=True, help_text='Starting U position (1-based)', null=True)),
                ('rack_unit_height', models.PositiveIntegerField(default=1, help_text='Number of U units occupied', validators=[django.core.validators.MinValueValidator(1)])),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="e.g., 'eth0', 'Gi0/0/1'", max_length=255)),
                ('interface_type', models.CharField(choices=[('ethernet', 'Ethernet'), ('wifi', 'WiFi/WLAN'), ('serial', 'Serial'), ('usb', 'USB'), ('optical', 'Optical Fiber'), ('other', 'Other')], max_length=50)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('mac_address', models.CharField(blank=True, max_length=17, null=True)),
                ('vlan_id', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='inventory.device')),
            ],
            options={
                'ordering': ['device', 'name'],
                'unique_together': {('device', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_type', models.CharField(choices=[('physical', 'Physical Cable'), ('logical', 'Logical Link'), ('vlan', 'VLAN Trunk'), ('wireless', 'Wireless')], default='physical', max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('destination_interface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_connections', to='inventory.interface')),
                ('source_interface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_connections', to='inventory.interface')),
            ],
            options={
                'ordering': ['source_interface', 'destination_interface'],
                'unique_together': {('source_interface', 'destination_interface')},
            },
        ),
        migrations.AddIndex(
            model_name='interface',
            index=models.Index(fields=['device'], name='inventory_i_device_idx'),
        ),
        migrations.AddIndex(
            model_name='interface',
            index=models.Index(fields=['ip_address'], name='inventory_i_ip_addr_idx'),
        ),
        migrations.AddIndex(
            model_name='device',
            index=models.Index(fields=['name'], name='inventory_d_name_idx'),
        ),
        migrations.AddIndex(
            model_name='device',
            index=models.Index(fields=['device_type'], name='inventory_d_device__idx'),
        ),
        migrations.AddIndex(
            model_name='device',
            index=models.Index(fields=['ip_address'], name='inventory_d_ip_addr_idx'),
        ),
        migrations.AddIndex(
            model_name='connection',
            index=models.Index(fields=['source_interface'], name='inventory_c_source__idx'),
        ),
        migrations.AddIndex(
            model_name='connection',
            index=models.Index(fields=['destination_interface'], name='inventory_c_destin_idx'),
        ),
    ]
