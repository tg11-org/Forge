from django.contrib import admin
from .models import HostingPlan


@admin.register(HostingPlan)
class HostingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price_monthly', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created_at', 'updated_at']

