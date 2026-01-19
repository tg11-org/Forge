from django.contrib import admin
from .models import PricingPlan, PricingFeature


class PricingFeatureInline(admin.TabularInline):
    model = PricingFeature
    extra = 1
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'is_featured', 'is_active', 'display_order']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [PricingFeatureInline]


@admin.register(PricingFeature)
class PricingFeatureAdmin(admin.ModelAdmin):
    list_display = ['plan', 'feature_text', 'is_included', 'display_order']
    list_filter = ['is_included', 'plan']
    search_fields = ['feature_text']
    readonly_fields = ['id', 'created_at', 'updated_at']

