from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class CustomUserManagerTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="testpass")

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
