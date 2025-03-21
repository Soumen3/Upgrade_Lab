from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('repositories/', views.repository_list, name='repository_list'),
    path('repositories/<int:pk>/', views.repository_detail, name='repository_detail'),
    path('repositories/<int:repository_id>/files/<int:file_id>/', views.file_detail, name='file_detail'),
    path('repositories/<int:pk>/download/', views.download_repository, name='download_repository'),
    path('repository/upload/', views.upload_repository, name='upload_repository'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)