from rest_framework import serializers

from user_app.validators import date_of_birth_validator


class LoginResponseSchema(serializers.Serializer):
    status = serializers.CharField(max_length=20)
    refresh = serializers.CharField(max_length=1000)
    access_token = serializers.CharField(max_length=1000)


class LoginErrorResponseSchema(serializers.Serializer):
    status = serializers.CharField(max_length=20, required=True)
    description = serializers.CharField(max_length=250, required=True)


class RegisterResponseSchema(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=12)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)


class RegisterErrorResponseSchema(serializers.Serializer):
    field = serializers.CharField(max_length=250)


class ChangeUserRequestSchema(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()

    def validate(self, attrs):
        if not date_of_birth_validator(attrs["date_of_birth"]):
            raise serializers.ValidationError(
                {"status": "error", "description": "You should be at least 18 years old."}
            )
        return attrs


class ChangeAvatarRequestSchema(serializers.Serializer):
    avatar = serializers.ImageField()


class ChangeAvatarResponseSchema(serializers.Serializer):
    status = serializers.CharField(max_length=20, required=True)
    description = serializers.CharField(max_length=250, required=True)


class ChangeUserResponseSchema(serializers.Serializer):
    status = serializers.CharField(max_length=20, required=True)
    description = serializers.CharField(max_length=250, required=True)


class UserNotFoundResponseSchema(serializers.Serializer):
    status = serializers.CharField(max_length=20, required=True)
    description = serializers.CharField(max_length=250, required=True)
