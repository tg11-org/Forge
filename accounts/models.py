from django.db import models
from django.contrib.auth.models import User
from forge.models import BaseModel
from payments.models import BasePayment


class UserProfile(BaseModel):
    """
    Extended user profile with additional information.
    Uses UUID as primary key via BaseModel inheritance.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, help_text="Stripe customer ID")
    
    def __str__(self):
        return f"Profile for {self.user.username}"

    class Meta:
        ordering = ['user__username']


class PaymentMethod(BaseModel):
    """
    Saved payment methods for users.
    Supports credit/debit cards, Apple Pay, Google Pay, etc. via Stripe.
    Uses UUID as primary key via BaseModel inheritance.
    """
    PAYMENT_TYPE_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('apple_pay', 'Apple Pay'),
        ('google_pay', 'Google Pay'),
        ('link', 'Link'),
        ('us_bank_account', 'US Bank Account'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    stripe_payment_method_id = models.CharField(max_length=100, help_text="Stripe payment method ID")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='card')
    
    # Card details (for display purposes only, never store full card numbers)
    card_brand = models.CharField(max_length=20, blank=True, help_text="e.g., Visa, Mastercard")
    card_last4 = models.CharField(max_length=4, blank=True, help_text="Last 4 digits of card")
    card_exp_month = models.IntegerField(null=True, blank=True)
    card_exp_year = models.IntegerField(null=True, blank=True)
    
    # Billing details
    billing_name = models.CharField(max_length=200, blank=True)
    billing_email = models.EmailField(blank=True)
    billing_address_line1 = models.CharField(max_length=200, blank=True)
    billing_address_line2 = models.CharField(max_length=200, blank=True)
    billing_city = models.CharField(max_length=100, blank=True)
    billing_state = models.CharField(max_length=100, blank=True)
    billing_postal_code = models.CharField(max_length=20, blank=True)
    billing_country = models.CharField(max_length=2, blank=True, help_text="Two-letter country code")
    
    is_default = models.BooleanField(default=False, help_text="Default payment method for this user")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.payment_type == 'card' and self.card_brand and self.card_last4:
            return f"{self.card_brand} ending in {self.card_last4}"
        return f"{self.get_payment_type_display()}"

    class Meta:
        ordering = ['-is_default', '-created_at']
        
    def save(self, *args, **kwargs):
        # If this is set as default, unset other defaults for this user
        if self.is_default:
            PaymentMethod.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class Payment(BasePayment):
    """
    Payment transactions using django-payments.
    Integrates with Django's payment framework for handling various payment providers.
    Note: This uses django-payments' auto-incremented ID, not UUID, for compatibility.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    saved_payment_method = models.ForeignKey(
        PaymentMethod, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="The saved payment method used for this transaction"
    )
    
    def get_failure_url(self):
        """URL to redirect to on payment failure"""
        return '/payment/failure/'
    
    def get_success_url(self):
        """URL to redirect to on payment success"""
        return '/payment/success/'
    
    def get_purchased_items(self):
        """Return list of purchased items for display"""
        return [
            {
                'name': self.description or 'Service',
                'quantity': 1,
                'price': self.total,
                'currency': self.currency,
                'sku': 'FORGE-SERVICE',
            }
        ]


class Order(BaseModel):
    """
    Customer orders/subscriptions.
    Links to django-payments Payment model.
    Uses UUID as primary key via BaseModel inheritance.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Order details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Optional references to services/plans
    description = models.TextField(blank=True, help_text="What was purchased")
    
    # Metadata
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Order {str(self.id)[:8]} - {self.user.username if self.user else 'Guest'} - ${self.total_amount}"

    class Meta:
        ordering = ['-created_at']


