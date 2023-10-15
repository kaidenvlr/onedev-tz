import json
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, path, include
from rest_framework.test import APITestCase, URLPatternsTestCase

from apps.order_app.models import Order
from core import settings


class OrderTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/user/', include('apps.user_app.urls')),  # User Application
        path('api/order/', include('apps.order_app.urls')),  # Order Application
    ]

    def setUp(self):
        self.username = "+77013926883"
        self.password = "helloworld123@"
        self.first_name = "Hello"
        self.last_name = "World"
        self.date_of_birth = "2002-04-03"
        self.token = self.receive_token()
        self.files = []

        filenames = [
            os.path.join(settings.BASE_DIR, 'media/orders/hearts.jpg'),
            os.path.join(settings.BASE_DIR, 'media/orders/soyle.png')
        ]
        for filename in filenames:
            f = open(filename, mode='rb')
            fp = SimpleUploadedFile(name=filename, content=f.read(), content_type="image/jpg; image/png")
            self.files.append(fp)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def receive_token(self):
        response = self.client.post(
            reverse("user_register"),
            {
                "username": self.username,
                "password": self.password, "confirm_password": self.password,
                "first_name": self.first_name, "last_name": self.last_name,
                "date_of_birth": self.date_of_birth
            }
        )
        self.assertEqual(201, response.status_code)
        response = self.client.post(
            reverse("user_login"),
            {"username": self.username, "password": self.password}
        )
        self.assertEqual(200, response.status_code)
        return json.loads(response.content).get('access_token')

    def test_create_order(self):
        self.api_authentication()
        response = self.client.post(
            reverse("add-order"),
            {"images": self.files}
        )
        self.assertEqual(201, response.status_code)

    def test_create_no_user_order(self):
        response = self.client.post(
            reverse("add-order"),
            {"images": self.files}
        )
        self.assertEqual(201, response.status_code)

    def test_get_order(self):
        response = self.client.post(
            reverse("add-order"),
            {"images": self.files}
        )
        self.assertEqual(201, response.status_code)

        order_id = int(json.loads(response.content).get("id"))
        response = self.client.get(
            reverse('get-order'),
            {"order_id": order_id}
        )
        self.assertEqual(200, response.status_code)

    def test_get_order_error(self):
        response = self.client.get(
            reverse("get-order"),
            {"order_id": 1}
        )
        self.assertEqual(404, response.status_code)

    def test_get_orders(self):
        response = self.client.get(
            reverse("get-orders")
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), Order.objects.count())
