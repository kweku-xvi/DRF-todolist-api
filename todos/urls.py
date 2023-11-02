from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_and_list_todos, name='todos'),
    path('<int:pk>/', views.todo_details, name='todo-detail'),
]