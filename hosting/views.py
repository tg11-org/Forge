from django.shortcuts import render


def hosting_list(request):
    """List all hosting solutions"""
    return render(request, 'hosting/list.html')


def hosting_detail(request, hosting_id):
    """Hosting solution detail view"""
    return render(request, 'hosting/detail.html', {'hosting_id': hosting_id})
