from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from user_app.models import User
from user_app.parameters import user_id_parameter
from user_app.responses import get_user_response, get_user_error_response, \
    get_users_response
from user_app.serializers import UserSerializer


@swagger_auto_schema(
    methods=["get"],
    manual_parameters=[user_id_parameter],
    responses={
        200: get_user_response,
        404: get_user_error_response
    }
)
@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def get_user(request: Request):
    user_id = request.query_params.get("user_id")
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return Response({'status': 'error', 'description': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['get'],
    responses={
        200: get_users_response
    }
)
@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def get_users(request: Request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
