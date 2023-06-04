from django.contrib import admin
from . import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'address', 'postcode']
    raw_id_fields = ['members']
    list_filter = ['postcode']
    search_fields = ['id', 'title', 'description', 'address', 'postcode']


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image', 'date', 'image_tag']
    raw_id_fields = ['organizations']
    fields = ['image_tag', 'title', 'description', 'image', 'date', 'organizations']
    list_filter = ['date', 'title']
    search_fields = ['id', 'title', 'description', 'date']
    readonly_fields = ['image_tag']
