from django import forms
import django.contrib.auth.models as dj_auth_models
import django.contrib.auth.forms as dj_auth_forms
from django.core.validators import validate_email
from . import models


class EmailAuthenticationForm(dj_auth_forms.AuthenticationForm):
    username = dj_auth_forms.UsernameField(
        widget=forms.EmailInput(attrs={'autofocus': True}),
        label="Email", validators=[validate_email])
    error_messages = {
        'invalid_login': "Please enter a correct email and password",
        'inactive': "This account is inactive.",
    }


class UserRegistrationForm(dj_auth_forms.UserCreationForm):
    username = dj_auth_forms.UsernameField(
        widget=forms.EmailInput(attrs={'autofocus': True}),
        label="Email", validators=[validate_email])


class UserEditForm(forms.ModelForm):
    class Meta:
        model = dj_auth_models.User
        fields = ['first_name', 'last_name']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['date_of_birth', 'photo']
