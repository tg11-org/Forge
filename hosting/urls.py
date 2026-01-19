from django.urls import path
from . import views

app_name = 'hosting'

urlpatterns = [
    path('', views.hosting_list, name='list'),
    path('<uuid:hosting_id>/', views.hosting_detail, name='detail'),
]
