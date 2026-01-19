from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Payment Methods
    path('payment-methods/', views.payment_methods, name='payment_methods'),
    path('payment-methods/add/', views.add_payment_method, name='add_payment_method'),
    path('payment-methods/<uuid:payment_method_id>/delete/', views.delete_payment_method, name='delete_payment_method'),
    path('payment-methods/<uuid:payment_method_id>/set-default/', views.set_default_payment_method, name='set_default_payment_method'),
    
    # Django-payments URLs (handles Stripe callbacks, etc.)
    path('payments/', include('payments.urls')),
]
