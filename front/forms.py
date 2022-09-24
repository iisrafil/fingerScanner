from django.forms import ModelForm;
from django.contrib.auth.forms import UserCreationForm;
from django.contrib.auth.models import User;
from django import forms

from front.models import *;

class CreateUserForm(UserCreationForm):
    # address = forms.CharField(max_length=100);
    type = forms.ChoiceField(choices=(
        ("owner", "Owner"), ("law", "Law"),
    ));
    class Meta(UserCreationForm.Meta):
        model = Account;
        fields = UserCreationForm.Meta.fields + ("email", "address");
        # fields = "__all__";

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Account;
        fields = ("username", "email", "address");

class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle;
        fields = "__all__";# [f.name for f in Vehicle._meta.get_fields()];
        exclude = ("approved", );

class DriverForm(ModelForm):
    class Meta:
        model = Driver;
        fields = "__all__";# [f.name for f in Driver._meta.get_fields()];
        exclude = ("approved", "vehicles");
    # vehicles = forms.ModelMultipleChoiceField(
    #     queryset=None,
    #     widget=forms.CheckboxSelectMultiple
    # );
    # def __init__(self, *args, **kwargs):
    #     self.pk = kwargs.pop("pk")
    #     super(DriverForm, self).__init__(*args, **kwargs)
    #     self.fields['vehicles'].queryset = Vehicle.objects.filter(driver_det__id=self.pk);