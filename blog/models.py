from django.db import models
from django.utils.text import slugify
from inventory.models import Device
from visualization.models import Diagram


class Article(models.Model):
    """Rich text documentation article"""
    
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField(help_text="Markdown or HTML content")
    description = models.CharField(max_length=500, blank=True, null=True)
    
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles'
    )
    
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:article-detail', kwargs={'slug': self.slug})


class ArticleEmbed(models.Model):
    """Embeds diagrams or device information within an article"""
    
    EMBED_TYPES = [
        ('diagram', 'Diagram'),
        ('device', 'Device'),
        ('mermaid', 'Mermaid Code'),
        ('chart', 'Chart/Graph'),
    ]
    
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='embeds'
    )
    
    embed_type = models.CharField(max_length=50, choices=EMBED_TYPES)
    
    # Optional: reference to a diagram
    diagram = models.ForeignKey(
        Diagram,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='article_embeds'
    )
    
    # Optional: reference to a device
    device = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='article_embeds'
    )
    
    # Custom mermaid code (if embed_type is 'mermaid')
    mermaid_code = models.TextField(blank=True, null=True)
    
    # Display options
    width = models.CharField(
        max_length=50,
        default='100%',
        help_text="e.g., '100%', '600px'"
    )
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order within article")
    
    class Meta:
        ordering = ['article', 'order']
        unique_together = [['article', 'order']]
    
    def __str__(self):
        return f"{self.article.title} - {self.get_embed_type_display()}"
