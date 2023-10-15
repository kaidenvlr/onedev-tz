from drf_yasg import openapi

from apps.user_app.schemas import LoginResponseSchema, RegisterResponseSchema, RegisterErrorResponseSchema, \
    StatusDescriptionResponseSchema
from apps.user_app.serializers import UserSerializer

login_user_response = openapi.Response('Login Response', LoginResponseSchema)
login_404_error_response = openapi.Response('Incorrect Credentials', StatusDescriptionResponseSchema)
login_400_error_response = openapi.Response('Provide correct credentials', StatusDescriptionResponseSchema)

register_user_response = openapi.Response("Register Response", RegisterResponseSchema)
register_error_response = openapi.Response("Bad request", RegisterErrorResponseSchema)

change_user_response = openapi.Response("Change user information response", StatusDescriptionResponseSchema)
change_avatar_response = openapi.Response("Change user's avatar response", StatusDescriptionResponseSchema)
change_password_response = openapi.Response("Change password response", StatusDescriptionResponseSchema)
change_password_error_response = openapi.Response("Bad request", StatusDescriptionResponseSchema)

get_user_response = openapi.Response("Get User information", UserSerializer)
get_user_error_response = openapi.Response("User not found", StatusDescriptionResponseSchema)
get_users_response = openapi.Response("Get users", UserSerializer(many=True))
