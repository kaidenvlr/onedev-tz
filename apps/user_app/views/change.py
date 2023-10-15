from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from apps.user_app.responses import change_user_response, change_avatar_response, change_password_response, \
    change_password_error_response
from apps.user_app.schemas import ChangeUserRequestSchema, ChangePasswordRequestSchema
from apps.user_app.validators import date_of_birth_validator


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


@swagger_auto_schema(
    methods=["patch"],
    request_body=ChangePasswordRequestSchema,
    responses={
        202: change_password_response,
        400: change_password_error_response
    }
)
@api_view(('PATCH',))
@permission_classes((permissions.IsAuthenticated,))
def change_password(request: Request):
    old_password = request.data.get("old_password")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")
    user = request.user
    if user.check_password(old_password) and password == confirm_password:
        user.set_password(password)
        user.save()
        return Response(
            data={"status": "ok", "description": "Password has been changed"},
            status=status.HTTP_202_ACCEPTED
        )
    elif password != confirm_password:
        return Response(
            data={"status": "error", "description": "Passwords didn't match"},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        data={"status": "error", "description": "Old password is incorrect"},
        status=status.HTTP_400_BAD_REQUEST
    )
