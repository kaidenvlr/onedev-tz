import datetime

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.models import TokenUser


def age(dob):
    today = datetime.date.today()
    years = today.year - dob.year
    if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
        years -= 1
    return years


def get_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh.token),
        'access': str(refresh.access_token)
    }
