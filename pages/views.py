from django.shortcuts import render


def home(request):
    """Home page view"""
    return render(request, 'pages/home.html')


def about(request):
    """About page view"""
    return render(request, 'pages/about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'pages/contact.html')
