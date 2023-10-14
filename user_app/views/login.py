from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from user_app.models import User
from user_app.responses import login_user_response, login_404_error_response, login_400_error_response, \
    register_user_response
from user_app.serializers import RegisterSerializer, LoginSerializer
from user_app.utils import get_tokens_for_user


@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body=LoginSerializer,
    responses={
        200: login_user_response,
        400: login_400_error_response,
        404: login_404_error_response
    }
)
@api_view(("POST",))
@permission_classes((permissions.AllowAny,))
def login(request: Request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            data={
                "status": "error",
                "description": "Please provide correct credentials"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            data={
                "status": "error",
                "description": "Invalid credentials"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    refresh = get_tokens_for_user(user)
    return Response(
        data={
            'status': 'ok',
            'refresh': refresh["refresh"],
            'access_token': refresh["access"]
        },
        status=status.HTTP_200_OK
    )
