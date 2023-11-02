from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Todo


class TodosAPITestCase(APITestCase):
    def create_todo(self):
        sample_todos = {
            'title':'test',
            'desc': 'hello world'
        }
        response = self.client.post(reverse('todos'), sample_todos)

        return response

    def authenticate(self):
        self.client.post(reverse('register'), {'username':'username', 'email':'email@gmail.com', 'password':'password'})
        response = self.client.post(reverse('login'), {"email":"email@gmail.com", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")



class TestListCreateTodos(TodosAPITestCase):

    def test_should_not_create_todo_with_no_user_authentication(self):
        response = self.create_todo()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_should_create_todo(self):
        self.authenticate()
        previous_todo_count = Todo.objects.all().count()
        
        response = self.create_todo()

        self.assertEqual(Todo.objects.all().count(), previous_todo_count+1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['desc'], 'hello world')

    
    def test_retrieves_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        self.create_todo()

        res = self.client.get(reverse('todos'))
        self.assertEqual(len(res.data), 1)

