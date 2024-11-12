from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
        path('chatbot/', views.chatbot, name='chatbot'),
        path('user/<int:id>/<str:username>/', views.user_profile, name='user_profile'),

]