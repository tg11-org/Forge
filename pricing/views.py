from django.shortcuts import render


def pricing_index(request):
    """Pricing page view"""
    return render(request, 'pricing/index.html')
