import datetime
import re

from user_app.utils import age


def phone_number_validator(phone_number: str):
    pattern = r"^(\+7)(\d{3})(\d{3})(\d{2})(\d{2})$"
    return re.match(pattern, phone_number)


def date_of_birth_validator(date_of_birth: str):
    y, m, d = map(int, date_of_birth.split('-'))
    dob = datetime.date(year=y, month=m, day=d)
    if age(dob) < 18:
        return False
    return True
