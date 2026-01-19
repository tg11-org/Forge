# Payment Integration Guide

## Overview

TG11 Forge includes comprehensive payment processing capabilities using **django-payments** and **Stripe**, supporting multiple payment methods including credit cards, Apple Pay, Google Pay, Link, and US bank accounts.

## Features

### 💳 Saved Payment Methods
- Users can save multiple payment methods for future transactions
- Set default payment method for one-click checkout
- Securely manage and remove payment methods
- All payment data stored with UUID primary keys

### 🔐 Security
- PCI-compliant payment handling via Stripe
- No sensitive card data stored on your servers
- Only card brand, last 4 digits, and expiration stored for display
- Full billing address support

### 🎨 Supported Payment Methods
- Credit & Debit Cards (Visa, Mastercard, Amex, Discover, etc.)
- Apple Pay (for iOS/macOS users)
- Google Pay  
- Link (Stripe's one-click payment)
- US Bank Accounts (ACH)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Stripe

Sign up for a Stripe account at [stripe.com](https://stripe.com) and get your API keys.

Set environment variables:

```bash
export STRIPE_SECRET_KEY="sk_test_..."
export STRIPE_PUBLISHABLE_KEY="pk_test_..."
export PAYMENT_HOST="localhost:8000"  # Your domain
export PAYMENT_USES_SSL="False"  # Set to True in production with HTTPS
```

### 3. Run Migrations

```bash
python manage.py migrate
```

## Models

### UserProfile
Extended user profile with Stripe customer ID and additional information.

**Fields:**
- `id` (UUID): Primary key
- `user` (OneToOne): Link to Django User
- `phone`: Phone number
- `company`: Company name
- `stripe_customer_id`: Stripe customer ID
- `created_at`, `updated_at`: Timestamps

### PaymentMethod
Saved payment methods for users.

**Fields:**
- `id` (UUID): Primary key
- `user` (ForeignKey): Owner
- `stripe_payment_method_id`: Stripe payment method ID
- `payment_type`: card, apple_pay, google_pay, link, us_bank_account
- `card_brand`, `card_last4`, `card_exp_month`, `card_exp_year`: Card display info
- `billing_*`: Billing address fields
- `is_default`: Whether this is the default payment method
- `is_active`: Whether this payment method is active
- `created_at`, `updated_at`: Timestamps

### Payment (django-payments)
Payment transactions handled by django-payments framework.

**Key Fields:**
- `user`: User making the payment
- `saved_payment_method`: The PaymentMethod used
- `status`: waiting, preauth, confirmed, rejected, refunded, error, input
- `variant`: Payment provider (stripe)
- `total`, `currency`: Amount and currency
- `description`: What was purchased
- `billing_*`: Billing information

### Order
Customer orders linking to payments.

**Fields:**
- `id` (UUID): Primary key  
- `user`: Customer
- `payment`: Link to Payment transaction
- `payment_method`: Saved PaymentMethod used
- `total_amount`, `currency`: Order amount
- `status`: pending, processing, completed, failed, refunded, cancelled
- `description`: Order details
- `created_at`, `updated_at`: Timestamps

## URLs

```python
# Profile
/accounts/profile/

# Payment Methods Management
/accounts/payment-methods/                          # List saved methods
/accounts/payment-methods/add/                      # Add new method
/accounts/payment-methods/<uuid>/delete/            # Remove method
/accounts/payment-methods/<uuid>/set-default/       # Set as default

# Django-payments (Stripe callbacks)
/accounts/payments/                                  # Payment processing
```

## Usage Examples

### Create a Payment

```python
from accounts.models import Payment, Order
from decimal import Decimal

# Create a payment
payment = Payment.objects.create(
    user=request.user,
    variant='stripe',
    total=Decimal('99.99'),
    currency='USD',
    description='Professional Plan - Monthly'
)

# Create associated order
order = Order.objects.create(
    user=request.user,
    payment=payment,
    total_amount=payment.total,
    currency=payment.currency,
    status='pending',
    description='Professional Plan Subscription'
)

# Get payment URL for user
payment_url = payment.get_process_url()
```

### Use Saved Payment Method

```python
from accounts.models import PaymentMethod

# Get user's default payment method
default_method = PaymentMethod.objects.filter(
    user=request.user,
    is_default=True,
    is_active=True
).first()

if default_method:
    # Use saved method for payment
    payment = Payment.objects.create(
        user=request.user,
        saved_payment_method=default_method,
        variant='stripe',
        total=Decimal('99.99'),
        currency='USD'
    )
```

### Save New Payment Method

This is typically done via Stripe.js on the frontend:

```javascript
// Frontend (with Stripe.js)
const stripe = Stripe('pk_test_...');
const elements = stripe.elements();
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');

// On form submit
const {paymentMethod} = await stripe.createPaymentMethod({
    elements,
    params: {
        billing_details: {
            name: 'Customer Name',
            email: 'customer@example.com'
        }
    }
});

// Send paymentMethod.id to your backend
fetch('/api/save-payment-method/', {
    method: 'POST',
    body: JSON.stringify({
        payment_method_id: paymentMethod.id
    })
});
```

```python
# Backend view to save payment method
import stripe
from accounts.models import PaymentMethod, UserProfile

def save_payment_method(request):
    pm_id = request.POST.get('payment_method_id')
    
    # Attach to Stripe customer
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if not profile.stripe_customer_id:
        customer = stripe.Customer.create(
            email=request.user.email,
            name=request.user.get_full_name()
        )
        profile.stripe_customer_id = customer.id
        profile.save()
    
    stripe.PaymentMethod.attach(
        pm_id,
        customer=profile.stripe_customer_id
    )
    
    # Get payment method details
    pm = stripe.PaymentMethod.retrieve(pm_id)
    
    # Save to database
    PaymentMethod.objects.create(
        user=request.user,
        stripe_payment_method_id=pm.id,
        payment_type='card',
        card_brand=pm.card.brand,
        card_last4=pm.card.last4,
        card_exp_month=pm.card.exp_month,
        card_exp_year=pm.card.exp_year,
        billing_name=pm.billing_details.name,
        billing_email=pm.billing_details.email
    )
```

## Admin Interface

All payment-related models are registered in Django admin:

- **UserProfile**: View and edit user profiles
- **PaymentMethod**: Manage saved payment methods
- **Payment**: View payment transactions (from django-payments)
- **Order**: Manage customer orders

Access at: `http://localhost:8000/admin/`

## Testing

### Test Cards (Stripe Test Mode)

```
Success:          4242 4242 4242 4242
Requires Auth:    4000 0025 0000 3155
Declined:         4000 0000 0000 9995
```

Use any future expiration date and any 3-digit CVC.

### Test Payment Flow

1. Create a test user
2. Navigate to `/accounts/payment-methods/`
3. Add a test card
4. Create a test payment/order
5. Process payment via Stripe
6. Verify in admin interface

## Production Checklist

- [ ] Switch to Stripe live API keys
- [ ] Set `PAYMENT_USES_SSL=True`
- [ ] Configure `PAYMENT_HOST` to your production domain
- [ ] Set up Stripe webhooks for payment status updates
- [ ] Enable Stripe Radar for fraud detection
- [ ] Configure currency and supported payment methods in Stripe Dashboard
- [ ] Test Apple Pay/Google Pay with real devices
- [ ] Set up proper error handling and logging
- [ ] Implement email notifications for payments
- [ ] Regular backup of payment/order data

## Webhooks

To handle Stripe webhooks (payment confirmations, refunds, etc.):

1. Set up webhook endpoint in Stripe Dashboard
2. Point to: `https://yourdomain.com/accounts/payments/process/stripe/`
3. Select events to listen for:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
   - `charge.refunded`

## Security Best Practices

1. **Never store full card numbers** - Only last 4 digits
2. **Use Stripe.js** - Handle sensitive data on Stripe's servers
3. **Validate on backend** - Don't trust client-side validation alone
4. **Use HTTPS in production** - Required for Apple Pay/Google Pay
5. **Implement rate limiting** - Prevent payment API abuse
6. **Log all transactions** - For auditing and troubleshooting
7. **Regular security audits** - Review payment flow periodically

## Troubleshooting

### "Payment method not found"
- Ensure payment method is attached to Stripe customer
- Check `stripe_payment_method_id` is correct

### "Customer not found"
- Create Stripe customer first via `UserProfile`
- Ensure `stripe_customer_id` is saved

### Apple Pay/Google Pay not showing
- Requires HTTPS (not localhost)
- Must be configured in Stripe Dashboard
- User must have compatible device

## Support

For issues:
1. Check [Stripe documentation](https://stripe.com/docs)
2. Review [django-payments docs](https://django-payments.readthedocs.io/)
3. Check Django logs for errors
4. Review Stripe Dashboard for payment details
