# Generated migration for visualization app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('diagram_type', models.CharField(choices=[('network', 'Network Topology'), ('rack', 'Rack Elevation'), ('process', 'Process Flow'), ('custom', 'Custom')], max_length=50)),
                ('mermaid_code', models.TextField(blank=True, help_text='Mermaid.js diagram code for flowcharts, etc.', null=True)),
                ('is_published', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('devices', models.ManyToManyField(blank=True, related_name='diagrams', to='inventory.device')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='diagram',
            index=models.Index(fields=['name'], name='visualizatio_name_idx'),
        ),
        migrations.AddIndex(
            model_name='diagram',
            index=models.Index(fields=['diagram_type'], name='visualizatio_diagram__idx'),
        ),
    ]
