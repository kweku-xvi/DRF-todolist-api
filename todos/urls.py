from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_todo, name='create'),
    path('list/', views.list_todos, name='list-todos'),
    path('<int:pk>/', views.get_todo, name='get-one-todo'),
    path('<int:pk>/update/', views.update_todo, name='update-todo'),
    path('<int:pk>/delete/', views.delete_todo, name='delete-todo'),
]