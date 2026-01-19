from django.shortcuts import render


def service_list(request):
    """List all services"""
    return render(request, 'services/list.html')


def service_detail(request, service_id):
    """Service detail view"""
    return render(request, 'services/detail.html', {'service_id': service_id})
