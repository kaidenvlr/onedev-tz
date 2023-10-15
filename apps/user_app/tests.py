import json
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, path, include
from rest_framework.test import APITestCase, URLPatternsTestCase

from core import settings


class UserTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/user/', include('apps.user_app.urls')),  # User Application
        path('api/order/', include('apps.order_app.urls')),  # Order Application
    ]

    def setUp(self):
        self.token_user = "+77066342342"
        self.token_password = "helloworld123@"
        self.token_first_name = "Super"
        self.token_last_name = "User"
        self.token_date_of_birth = "2002-04-03"

        self.username = "+77013926883"
        self.password = "helloworld123@"
        self.first_name = "Hello"
        self.last_name = "World"
        self.date_of_birth = "2002-04-03"
        self.token = self.receive_token()
        self.avatar = SimpleUploadedFile(
            name="avatar_example.jpg",
            content=open(os.path.join(settings.BASE_DIR, 'media/orders/hearts.jpg'), mode="rb").read(),
            content_type="image/jpg"
        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def receive_token(self):
        response = self.client.post(
            reverse("user_register"),
            {
                "username": self.token_user,
                "password": self.token_password, "confirm_password": self.token_password,
                "first_name": self.token_first_name, "last_name": self.token_last_name,
                "date_of_birth": self.token_date_of_birth
            }
        )
        # print(response.content)
        self.assertEqual(201, response.status_code)

        response = self.client.post(
            reverse("user_login"),
            {"username": self.token_user, "password": self.token_password}
        )
        self.assertEqual(200, response.status_code)
        return json.loads(response.content).get('access_token')

    def test_create_user(self):
        response = self.client.post(
            reverse("user_register"),
            {
                "username": self.username,
                "password": self.password, "confirm_password": self.password,
                "first_name": self.first_name, "last_name": self.last_name,
                "date_of_birth": self.date_of_birth
            }
        )
        # print(response.content)
        self.assertEqual(201, response.status_code)

    def test_login_user(self):
        response = self.client.post(
            reverse("user_login"),
            {"username": self.token_user, "password": self.token_password}
        )
        self.assertEqual(200, response.status_code)

    def test_change_user(self):
        self.api_authentication()
        response = self.client.patch(
            reverse("user_change_info"),
            {
                "first_name": "Hi!",
                "date_of_birth": "2004-03-16",
            }
        )
        self.assertEqual(202, response.status_code)

    def test_change_user_error(self):
        self.api_authentication()
        response = self.client.patch(
            reverse("user_change_info"),
            {
                "date_of_birth": "2023-01-01"
            }
        )
        self.assertEqual(400, response.status_code)

    def test_change_avatar(self):
        self.api_authentication()
        response = self.client.patch(
            reverse("user_change_avatar"),
            {
                "avatar": self.avatar
            }
        )
        self.assertEqual(202, response.status_code)

    def test_change_password_incorrect_password(self):
        self.api_authentication()
        response = self.client.patch(
            reverse("user_change_password"),
            {
                "old_password": self.token_password+"...",
                "password": self.password,
                "confirm_password": self.password
            }
        )
        self.assertEqual(400, response.status_code)

    def test_change_password_password_didnt_match(self):
        self.api_authentication()
        response = self.client.patch(
            reverse("user_change_password"),
            {
                "old_password": self.token_password,
                "password": self.password + "123",
                "confirm_password": self.password
            }
        )
        self.assertEqual(400, response.status_code)

    def test_change_password(self):
        self.api_authentication()
        response = self.client.patch(
            reverse("user_change_password"),
            {
                "old_password": self.token_password,
                "password": self.password,
                "confirm_password": self.password
            }
        )
        self.assertEqual(202, response.status_code)

    def test_get_user(self):
        response = self.client.get(
            reverse("user_get"),
            {
                "user_id": 1
            }
        )
        self.assertEqual(200, response.status_code)

    def test_get_user_error(self):
        response = self.client.get(
            reverse("user_get"),
            {
                "user_id": 126378
            }
        )
        self.assertEqual(404, response.status_code)

    def test_list_user(self):
        response = self.client.get(
            reverse("user_list")
        )
        self.assertEqual(200, response.status_code)
