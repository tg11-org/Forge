from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import PaymentMethod, UserProfile
import stripe


@login_required
def payment_methods(request):
    """List all saved payment methods for the logged-in user"""
    methods = PaymentMethod.objects.filter(user=request.user, is_active=True)
    return render(request, 'accounts/payment_methods.html', {
        'payment_methods': methods,
        'stripe_publishable_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
    })


@login_required
def add_payment_method(request):
    """Add a new payment method"""
    if request.method == 'POST':
        # This would integrate with Stripe Elements/Payment Element
        # For now, showing the template
        messages.info(request, 'Payment method integration ready. Configure Stripe API keys.')
        return redirect('accounts:payment_methods')
    
    return render(request, 'accounts/add_payment_method.html', {
        'stripe_publishable_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
    })


@login_required
def delete_payment_method(request, payment_method_id):
    """Delete a saved payment method"""
    method = get_object_or_404(PaymentMethod, id=payment_method_id, user=request.user)
    
    if request.method == 'POST':
        # Detach from Stripe if configured
        if hasattr(settings, 'STRIPE_SECRET_KEY') and settings.STRIPE_SECRET_KEY:
            try:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                stripe.PaymentMethod.detach(method.stripe_payment_method_id)
            except Exception as e:
                messages.warning(request, f'Could not detach from Stripe: {str(e)}')
        
        method.is_active = False
        method.save()
        messages.success(request, 'Payment method removed successfully.')
        return redirect('accounts:payment_methods')
    
    return render(request, 'accounts/confirm_delete_payment.html', {'method': method})


@login_required
def set_default_payment_method(request, payment_method_id):
    """Set a payment method as default"""
    method = get_object_or_404(PaymentMethod, id=payment_method_id, user=request.user)
    method.is_default = True
    method.save()
    messages.success(request, 'Default payment method updated.')
    return redirect('accounts:payment_methods')


@login_required
def profile(request):
    """User profile page"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

