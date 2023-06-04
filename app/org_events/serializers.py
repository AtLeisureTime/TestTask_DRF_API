from collections import OrderedDict
import django.contrib.auth as dj_auth
from rest_framework import serializers as rest_fw_serializers
import account.models as account_models
from . import models

User = dj_auth.get_user_model()


class UserSerializer(rest_fw_serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserProfileSerializer(rest_fw_serializers.ModelSerializer):
    username = rest_fw_serializers.CharField(source='user.username')
    first_name = rest_fw_serializers.CharField(source='user.first_name')
    last_name = rest_fw_serializers.CharField(source='user.last_name')

    class Meta:
        model = account_models.Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'date_of_birth', 'photo']


class OrganizationSerializerList(rest_fw_serializers.ModelSerializer):
    members = UserProfileSerializer(many=True, required=False)

    class Meta:
        model = models.Organization
        fields = '__all__'  # ['id', 'title', 'description', 'address', 'postcode', 'members']


class OrganizationSerializerCreate(rest_fw_serializers.ModelSerializer):
    members = rest_fw_serializers.PrimaryKeyRelatedField(
        many=True, allow_null=True, queryset=account_models.Profile.objects.all())

    class Meta:
        model = models.Organization
        fields = '__all__'

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        newOrg = super().create(validated_data)
        if members:
            newOrg.members.set(members)
        return newOrg


class OrganizationSerializerListShort(rest_fw_serializers.ModelSerializer):
    members = UserProfileSerializer(many=True, required=False)

    class Meta:
        model = models.Organization
        fields = ['members']

    def to_representation(self, instance):
        org = super().to_representation(instance)
        return OrderedDict([('organization', str(instance)), ('members', org['members'])])


class EventSerializerList(rest_fw_serializers.ModelSerializer):
    organizations = OrganizationSerializerListShort(many=True, required=False)

    class Meta:
        model = models.Event
        fields = '__all__'  # ['id', 'title', 'description', 'organizations', 'image', 'date']


class EventSerializerCreate(rest_fw_serializers.ModelSerializer):
    organizations = rest_fw_serializers.PrimaryKeyRelatedField(
        many=True, allow_null=True, queryset=models.Organization.objects.all())

    class Meta:
        model = models.Event
        fields = '__all__'

    def create(self, validated_data):
        orgs = validated_data.pop('organizations', [])
        newEvent = super().create(validated_data)
        if orgs:
            newEvent.organizations.set(orgs)
        return newEvent
