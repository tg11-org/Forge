from django.contrib import admin
from .models import UserProfile, PaymentMethod, Payment, Order


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'company', 'stripe_customer_id', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'company']
    readonly_fields = ['id', 'created_at', 'updated_at', 'stripe_customer_id']
    raw_id_fields = ['user']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_type', 'card_brand', 'card_last4', 'is_default', 'is_active', 'created_at']
    list_filter = ['payment_type', 'is_default', 'is_active', 'card_brand']
    search_fields = ['user__username', 'user__email', 'card_last4', 'billing_name', 'billing_email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'stripe_payment_method_id']
    raw_id_fields = ['user']
    
    fieldsets = (
        ('Payment Method', {
            'fields': ('id', 'user', 'stripe_payment_method_id', 'payment_type', 'is_default', 'is_active')
        }),
        ('Card Information', {
            'fields': ('card_brand', 'card_last4', 'card_exp_month', 'card_exp_year'),
            'classes': ('collapse',)
        }),
        ('Billing Information', {
            'fields': ('billing_name', 'billing_email', 'billing_address_line1', 'billing_address_line2',
                      'billing_city', 'billing_state', 'billing_postal_code', 'billing_country'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total', 'currency', 'variant', 'created']
    list_filter = ['status', 'variant', 'currency', 'created']
    search_fields = ['user__username', 'user__email', 'description', 'transaction_id']
    readonly_fields = ['created', 'modified', 'transaction_id']
    raw_id_fields = ['user', 'saved_payment_method']
    date_hierarchy = 'created'
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('user', 'variant', 'status', 'fraud_status', 'fraud_message')
        }),
        ('Amount', {
            'fields': ('currency', 'total', 'tax', 'delivery', 'captured_amount')
        }),
        ('Details', {
            'fields': ('description', 'billing_first_name', 'billing_last_name', 'billing_address_1',
                      'billing_address_2', 'billing_city', 'billing_postcode', 'billing_country_code',
                      'billing_country_area', 'billing_email')
        }),
        ('Saved Payment Method', {
            'fields': ('saved_payment_method',),
            'classes': ('collapse',)
        }),
        ('Transaction Info', {
            'fields': ('transaction_id', 'token', 'extra_data'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id_short', 'user', 'total_amount', 'currency', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['user__username', 'user__email', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['user', 'payment', 'payment_method']
    date_hierarchy = 'created_at'
    
    def id_short(self, obj):
        """Show shortened UUID for list display"""
        return str(obj.id)[:8] + '...'
    id_short.short_description = 'Order ID'
    
    def payment_status(self, obj):
        """Show payment status"""
        if obj.payment:
            return obj.payment.status
        return 'No payment'
    payment_status.short_description = 'Payment Status'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'user', 'status', 'total_amount', 'currency', 'description')
        }),
        ('Payment', {
            'fields': ('payment', 'payment_method')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


