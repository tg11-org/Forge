from django.contrib import admin
from .models import PortfolioItem


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'client_name', 'project_date', 'is_featured', 'is_published']
    list_filter = ['is_featured', 'is_published', 'project_date', 'created_at']
    search_fields = ['title', 'slug', 'description', 'client_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'project_date'

