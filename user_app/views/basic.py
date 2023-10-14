from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from user_app.models import User
from user_app.parameters import user_id_parameter
from user_app.responses import change_user_response, change_avatar_response
from user_app.schemas import ChangeUserRequestSchema
from user_app.serializers import UserSerializer
from user_app.validators import date_of_birth_validator


@swagger_auto_schema(
    methods=["get"],
    manual_parameters=[user_id_parameter]
)
@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def get_user(request: Request):
    user_id = request.query_params.get("user_id")
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def get_users(request: Request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=["patch"],
    request_body=ChangeUserRequestSchema,
    responses={
        202: change_user_response,
        400: change_user_response
    }
)
@api_view(('PATCH',))
@permission_classes((permissions.IsAuthenticated,))
def change_user_info(request: Request):
    data = request.data
    user = request.user.user

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.avatar = data.get('avatar', user.avatar)
    date = data.get('date_of_birth', user.date_of_birth)
    if date_of_birth_validator(date):
        user.date_of_birth = date
    else:
        return Response({"status": "error", "description": "You must be at least 18 years old"},
                        status=status.HTTP_400_BAD_REQUEST)

    user.save()

    return Response({"status": "ok", "description": "Changes set."}, status=status.HTTP_202_ACCEPTED)


@swagger_auto_schema(
    methods=["patch"],
    manual_parameters=[
        openapi.Parameter("avatar", openapi.IN_FORM, type=openapi.TYPE_FILE, description="New avatar")
    ],
    responses={
        202: change_avatar_response,
        400: change_avatar_response
    }
)
@api_view(('PATCH',))
@permission_classes((permissions.IsAuthenticated,))
@parser_classes((MultiPartParser,))
def change_avatar(request: Request):
    user = request.user.user
    user.avatar = request.data.get('avatar')
    user.save()

    return Response({"status": "ok", "description": "Avatar set."}, status=status.HTTP_202_ACCEPTED)
