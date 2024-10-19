from django.urls import path
from . import views

urlpatterns = [
    path('problems/', views.problem_list_view, name='problem_list'),
    path('problems/<int:pk>/', views.problem_detail_view, name='problem_detail'),
    path('post-problem/', views.post_problems, name='post_problem'),
]