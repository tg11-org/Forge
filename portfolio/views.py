from django.shortcuts import render


def portfolio_list(request):
    """List all portfolio items"""
    return render(request, 'portfolio/list.html')


def portfolio_detail(request, portfolio_id):
    """Portfolio item detail view"""
    return render(request, 'portfolio/detail.html', {'portfolio_id': portfolio_id})
