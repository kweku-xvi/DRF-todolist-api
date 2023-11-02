from django.shortcuts import render
from .serializers import TodoSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Todo
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated


#create todo
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_todo(request):
    if request.method == 'POST':
        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#list all todos
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_todos(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(owner=request.user)
        serializer = TodoSerializer(todos, many=True)

        return response.Response(serializer.data, status=status.HTTP_200_OK)



# list one todo
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_todo(request, pk):
    if request.method == 'GET':
        try:
            todo = Todo.objects.filter(owner=request.user).get(id=pk)
        except Todo.DoesNotExist:
            return response.Response({'message':'ID specified does not except'},status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo)

        return response.Response(serializer.data, status=status.HTTP_200_OK)


# update one todo 
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_todo(request, pk):
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            todo = Todo.objects.filter(owner=request.user).get(id=pk)
        except Todo.DoesNotExist:
            return response.Response({'message':'Todo object specified does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete one todo 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_todo(request, pk):
    try:
            todo = Todo.objects.filter(owner=request.user).get(id=pk)
    except Todo.DoesNotExist:
        return response.Response({'message':'Todo object specified does not exist'})

    if request.method == 'DELETE':
        todo.delete()

        return response.Response({'message':'Object has been deleted'}, status=status.HTTP_204_NO_CONTENT)