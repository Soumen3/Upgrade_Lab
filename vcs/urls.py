from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('repositories/', views.repository_list, name='repository_list'),
    path('repositories/<int:pk>/', views.repository_detail, name='repository_detail'),
    path('upload/', views.upload_repository, name='upload_repository'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)