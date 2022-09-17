from django.forms import ModelForm;
from django.contrib.auth.forms import UserCreationForm;
from django.contrib.auth.models import User;
from django import forms;

class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User;
        fields = UserCreationForm.Meta.fields + ("email", );