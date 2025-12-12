# Generated migration for blog app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0002_initial'),
        ('visualization', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('content', models.TextField(help_text='Markdown or HTML content')),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ArticleEmbed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('embed_type', models.CharField(choices=[('diagram', 'Diagram'), ('device', 'Device'), ('mermaid', 'Mermaid Code'), ('chart', 'Chart/Graph')], max_length=50)),
                ('mermaid_code', models.TextField(blank=True, null=True)),
                ('width', models.CharField(default='100%', help_text="e.g., '100%', '600px'", max_length=50)),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Order within article')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='embeds', to='blog.article')),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_embeds', to='inventory.device')),
                ('diagram', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_embeds', to='visualization.diagram')),
            ],
            options={
                'ordering': ['article', 'order'],
                'unique_together': {('article', 'order')},
            },
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['slug'], name='blog_articl_slug_idx'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['is_published'], name='blog_articl_is_publi_idx'),
        ),
    ]
