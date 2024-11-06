from django.urls import path
from . import views

urlpatterns = [
    path('problems/', views.problem_list_view, name='problem_list'),
    path('problem/<int:pk>/', views.problem_detail_view, name='problem_detail'),
    path('problem/<int:pk>/code_snippet/', views.get_code_snippet, name='get_code_snippet'),
    path('post-problem/', views.post_problems, name='post_problem'),
]