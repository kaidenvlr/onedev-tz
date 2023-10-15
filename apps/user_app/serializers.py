import datetime
from datetime import date

from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.user_app.models import User
from apps.user_app.utils import age
from apps.user_app.validators import phone_number_validator, date_of_birth_validator


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=12)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if not phone_number_validator(phone_number=attrs["username"]):
            raise serializers.ValidationError(
                {"username": "Phone number should be correct."}
            )
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=(
            UniqueValidator(queryset=DjangoUser.objects.all()),
            phone_number_validator,
        )
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=(
            validate_password,
        )
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )
    date_of_birth = serializers.DateField(
        write_only=True,
        required=True,
        validators=(
            date_of_birth_validator,
        )
    )
    avatar = serializers.ImageField(
        write_only=True,
        required=False,
    )

    class Meta:
        model = DjangoUser
        fields = (
            'id',
            'username',
            'password', 'confirm_password',
            'first_name', 'last_name', 'date_of_birth',
            'avatar',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'avatar': {'required': False}
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"}
            )

        if not phone_number_validator(phone_number=attrs["username"]):
            raise serializers.ValidationError(
                {"username": "Phone number should be correct."}
            )

        if not date_of_birth_validator(date_of_birth=attrs["date_of_birth"]):
            raise serializers.ValidationError(
                {"date_of_birth": "You must be at least 18 years old."}
            )
        return attrs

    def create(self, validated_data):
        django_user = DjangoUser.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        django_user.set_password(validated_data["password"])
        django_user.save()

        user = User.objects.get(django_user=django_user)

        user.first_name = validated_data["first_name"]
        user.last_name = validated_data["last_name"]
        user.phone_number = validated_data["username"]
        if validated_data.get("avatar", None) is not None:
            user.avatar = validated_data["avatar"]
        user.date_of_birth = validated_data["date_of_birth"]
        user.save()

        return django_user


class UserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'avatar', 'date_of_birth', 'age')

    def get_age(self, obj):
        date_of_birth = str(obj.date_of_birth)
        y, m, d = map(int, date_of_birth.split('-'))
        dob = datetime.date(year=y, month=m, day=d)
        return age(dob)
