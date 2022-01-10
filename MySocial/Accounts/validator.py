from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


# Phone Number Validator
def phoneNumberValidator(phone_number):
    if phone_number is None:
        raise ValidationError('User must have a phone number')

    elif len(phone_number) < 8:
        raise ValidationError('Phone Number Validation Error')


# Phone Regex
phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$',
                             message="Phone number must be entered in the format: '999999999'. Up to 15 digits "
                                     "allowed.")
