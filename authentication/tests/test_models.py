from rest_framework.test import APITestCase
from ..models import User

class TestModels(APITestCase):
    def test_creates_user(self):
        user = User.objects.create_user(username='test', email='test@user.com', password='1234')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@user.com')
        self.assertFalse(user.is_staff)


    def test_raises_error_with_message_with_no_username_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given username must be set"):
            User.objects.create_user(username='', email='test@user.com', password='1234')


    def test_raises_error_with_message_with_no_email_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given email must be set"):
            User.objects.create_user(username='test', email='', password='1234')

    
    def test_creates_superuser(self):
        user = User.objects.create_superuser(username='test', email='test@user.com', password='1234')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@user.com')
        self.assertTrue(user.is_staff)

    
    def test_raises_error_when_superuser_has_no_staff_privelleges(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(username='test', email='test@user.com', password='1234', is_staff=False)


    def test_raises_error_when_superuser_has_no_superuser_privelleges(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):
            User.objects.create_superuser(username='test', email='test@user.com', password='1234', is_superuser=False)