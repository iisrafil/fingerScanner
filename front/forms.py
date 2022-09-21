from django.forms import ModelForm;
from django.contrib.auth.forms import UserCreationForm;
from django.contrib.auth.models import User;
from django import forms

from front.models import Account;

class CreateUserForm(UserCreationForm):
    # address = forms.CharField(max_length=100);
    class Meta(UserCreationForm.Meta):
        model = Account;
        fields = UserCreationForm.Meta.fields + ("email", "address");
        # fields = "__all__";