from django.db import models
from django.core.validators import RegexValidator
from django.utils.html import mark_safe
import account.models as account_models


class Organization(models.Model):
    TITLE_LEN = 80
    DESCR_LEN = 200
    ADDR_LEN = 200
    POSTCODE_LEN = 6

    title = models.CharField(max_length=TITLE_LEN, blank=False)
    description = models.CharField(max_length=DESCR_LEN, blank=True)
    address = models.CharField(max_length=ADDR_LEN, blank=True)
    postcode = models.CharField(
        max_length=POSTCODE_LEN,
        validators=[RegexValidator('^[0-9]{6}$', 'Invalid postal code')],
    )
    members = models.ManyToManyField(account_models.Profile, related_name='organizations',
                                     blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.postcode}, {self.address}'


class Event(models.Model):
    TITLE_LEN = 80
    DESCR_LEN = 200
    IMAGE_UPLOAD_TO = 'events/%Y/%m/%d/'

    title = models.CharField(max_length=TITLE_LEN, blank=False)
    description = models.CharField(max_length=DESCR_LEN, blank=True)
    organizations = models.ManyToManyField(
        Organization, related_name='events', blank=True)
    image = models.ImageField(upload_to=IMAGE_UPLOAD_TO, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['title']

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')
        return mark_safe('No image')

    image_tag.short_description = 'Event image'
    image_tag.allow_tags = True

    def __str__(self):
        return self.title
