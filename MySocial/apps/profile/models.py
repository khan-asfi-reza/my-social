from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from apps.core.models import UUIDBaseModel


class ProfileManager(models.Manager):

    def create_profile(self, **kwargs):
        profile_picture = kwargs.pop("profile_picture", None)
        if type(profile_picture) in [bytes, bytearray]:
            print("")


# User's profile
class Profile(UUIDBaseModel):
    # User
    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                verbose_name='profile',
                                unique=True)
    # User profile Picture
    profile_picture = models.ImageField(blank=True, null=True)
    # User Cover Picture
    cover_picture = models.URLField(blank=True, null=True)
    # User's Bio
    bio = models.CharField(blank=True, max_length=312)
    # Users Location
    # Is Online
    online = models.BooleanField(default=False)
    # Last Online Time
    last_online = models.DateTimeField(auto_now=True)
    # Completed On-boarding
    is_on_boarding_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(
            self, *args, **kwargs
    ):
        print(self.profile_picture)
        print(type(self.profile_picture))
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User, dispatch_uid="create_user_profile")
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
