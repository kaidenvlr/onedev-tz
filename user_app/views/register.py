from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from user_app.models import User
from user_app.responses import register_user_response
from user_app.serializers import RegisterSerializer


@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def get_user(request: Request):
    id = request.query_params.get('id')

    user = User.objects.get(id=id)

    return user


class UserAPIView(APIView):
    authentication_classes = []
    schema = AutoSchema()
    permission_classes = (permissions.AllowAny,)

    def get(self, request: Request):
        id = request.query_params.get('id')
        user = User.objects.get(id=id)
        return user


@swagger_auto_schema(
    methods=['post'],
    request_body=RegisterSerializer,
    responses={
        201: register_user_response
    }
)
@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def register(request: Request, *args, **kwargs):
    user_serializer = RegisterSerializer(data=request.data)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save()
    return Response(user_serializer.data, status=status.HTTP_201_CREATED)
