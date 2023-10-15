from rest_framework import serializers

from apps.user_app.validators import date_of_birth_validator


class LoginResponseSchema(serializers.Serializer):
    status = serializers.CharField(max_length=20)
    refresh = serializers.CharField(max_length=1000)
    access_token = serializers.CharField(max_length=1000)


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


class ChangePasswordRequestSchema(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)


class StatusDescriptionResponseSchema(serializers.Serializer):
    status = serializers.CharField(max_length=20, required=True)
    description = serializers.CharField(max_length=250, required=True)
