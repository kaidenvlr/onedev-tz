from drf_yasg import openapi

from user_app.schemas import LoginResponseSchema, LoginErrorResponseSchema, RegisterResponseSchema, \
    ChangeUserResponseSchema, ChangeAvatarResponseSchema, UserNotFoundResponseSchema, RegisterErrorResponseSchema
from user_app.serializers import UserSerializer

login_user_response = openapi.Response('Login Response', LoginResponseSchema)
login_404_error_response = openapi.Response('Incorrect Credentials', LoginErrorResponseSchema)
login_400_error_response = openapi.Response('Provide correct credentials', LoginErrorResponseSchema)

register_user_response = openapi.Response("Register Response", RegisterResponseSchema)
register_error_response = openapi.Response("Bad request", RegisterErrorResponseSchema)

change_user_response = openapi.Response("Change user information response", ChangeUserResponseSchema)
change_avatar_response = openapi.Response("Change user's avatar response", ChangeAvatarResponseSchema)

get_user_response = openapi.Response("Get User information", UserSerializer)
get_user_error_response = openapi.Response("User not found", UserNotFoundResponseSchema)
get_users_response = openapi.Response("Get users", UserSerializer(many=True))
