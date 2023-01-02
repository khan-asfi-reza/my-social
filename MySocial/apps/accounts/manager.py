  
  
  
  
  
  
  
  
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

from .validator import phone_number_validator


# Custom User Model Manager
class UserManager(BaseUserManager):

    def create_user(self, username, phone_number, password, email=None):
        """
        Creates and saves a User with the given phone_number and password.
        """
        # Validates Phone Number
        phone_number_validator(phone_number)
        # Check if user exists
        user = self.model.objects.filter(phone_number=phone_number, username=username, )
        if user.exists():
            raise ValidationError('User already exists')
        # Creating user instance
        user = self.model(username=username)
        # Normalizing Email
        if email is not None:
            user = self.model(username=username, email=self.normalize_email(email), )
        # Set user password
        user.set_password(password)
        # Setting other information
        user.phone_number = phone_number
        user.save(using=self._db)
        return user

    # Creates staff user
    def create_staffuser(self, phone_number, username, password, email=None):
        # Creates a non super admin
        user = self.create_user(phone_number=phone_number, email=email, password=password,
                                username=username,
                                )
        user.is_staff = True
        user.verified = True
        user.save(using=self._db)
        return user

    # Creates Admin
    def create_superuser(self, phone_number, username, password, email=None):
        # Creates and saves a superuser with the given email and password.
        user = self.create_user(phone_number=phone_number, email=email, password=password,
                                username=username,
                                )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.verified = True
        user.save(using=self._db)
        return user
