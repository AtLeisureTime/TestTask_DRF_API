from django.db import models
import django.contrib.auth as dj_auth

User = dj_auth.get_user_model()


class Profile(models.Model):
    """ Additional user fields."""
    PHOTO_UPLOAD_TO = 'users/%Y/%m/%d/'

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=PHOTO_UPLOAD_TO, blank=True, null=True)
    # TODO: add other fields

    def __str__(self):
        return f'{self.user.username}'
