from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
        path('chatbot/', views.chatbot, name='chatbot'),
        path('user/<int:id>/<str:username>/', views.user_profile, name='user_profile'),
        path('user/<int:id>/<str:username>/add/', views.add_user_detail, name='add_user_detail'),
        path('user/<int:id>/<str:username>/social-media/', views.update_social_media, name='update_social_media'),
        path('search/', views.search, name='search'),
]