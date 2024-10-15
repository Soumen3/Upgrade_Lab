
from django.urls import path
from .views import repository_list, repository_detail

urlpatterns = [
    path('repositories/', repository_list, name='repository_list'),
    path('repositories/<int:pk>/', repository_detail, name='repository_detail'),
]