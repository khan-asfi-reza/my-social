from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from MySocial.models import UUIDBaseModel
from .manager import UserManager


# Custom User Model
class User(AbstractUser, UUIDBaseModel):

    # Phone Number
    phone_number = PhoneNumberField(unique=True)
    # Check for verification
    is_verified = models.BooleanField(default=False)
    # User Model Related
    REQUIRED_FIELDS = ['phone_number', 'email']

    # calling user manager class
    objects = UserManager()

    def get_name(self):
        return self.username

    def get_username(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username

