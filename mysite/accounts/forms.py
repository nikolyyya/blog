from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {"first_name": "Имя", "last_name": "Фамилия"}


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio", "location", "birth_date")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "birth_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
