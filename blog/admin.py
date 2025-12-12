from django.contrib import admin
from .models import Article, ArticleEmbed


class ArticleEmbedInline(admin.TabularInline):
    model = ArticleEmbed
    extra = 1
    fields = ['embed_type', 'diagram', 'device', 'order', 'caption']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    inlines = [ArticleEmbedInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Metadata', {
            'fields': ('author', 'is_published', 'created_at', 'updated_at')
        }),
    )


@admin.register(ArticleEmbed)
class ArticleEmbedAdmin(admin.ModelAdmin):
    list_display = ['article', 'embed_type', 'order', 'caption']
    list_filter = ['embed_type', 'article']
    search_fields = ['article__title', 'caption']
    ordering = ['article', 'order']
