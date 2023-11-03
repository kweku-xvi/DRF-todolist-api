from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_and_list_todos, name='todos'),
    path('<int:id>/', views.todo_details, name='todo-detail'),
]