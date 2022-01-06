from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from MySocial.models import UUIDBaseModel
from .manager import UserManager


def user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


# Custom User Model
class User(AbstractBaseUser,
           PermissionsMixin,
           UUIDBaseModel):
    # Name / User username
    username = models.CharField(max_length=128,
                                null=False,
                                blank=False,
                                unique=True)
    # Phone Number
    phone_number = PhoneNumberField()
    # Email
    email = models.EmailField(editable=True, null=True, blank=True, unique=True)
    # Check for verification
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['gender', 'phone_number']

    # calling user manager class
    objects = UserManager()

    def get_name(self):
        return self.username

    def get_username(self):
        return self.username

    def __str__(self):
        return self.username


user_model = get_user_model()


# Creates Profile After User is created
@receiver(post_save, sender=user_model)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from Profile.models import Profile
        profile = Profile(user=instance)
        if instance.gender == 1:
            profile.verified = True
        profile.save()


