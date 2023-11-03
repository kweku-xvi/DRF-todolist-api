from django.shortcuts import render
from .serializers import TodoSerializer
from rest_framework.decorators import api_view, permission_classes
from .models import Todo
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated


# create and list todos 
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_and_list_todos(request):
    if request.method == 'POST': # creating a todo
        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET': # retrieving all todos created by the current user
        todos = Todo.objects.filter(owner=request.user)
        serializer = TodoSerializer(todos, many=True)

        return response.Response(serializer.data, status=status.HTTP_200_OK)


# reading, updating and deleting todos
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_details(request, id):
    try:
        todo = Todo.objects.filter(owner=request.user).get(id=id)
    except Todo.DoesNotExist:
        return response.Response({'message':'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': # retrieving an object
        serializer = TodoSerializer(todo)

        return response.Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT' or request.method == 'PATCH': # updating an object
        serializer = TodoSerializer(todo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': # deleting an item
        todo.delete()

        return response.Response({'message':'Object has been deleted'}, status=status.HTTP_204_NO_CONTENT)