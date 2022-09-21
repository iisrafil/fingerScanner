from django.contrib import admin
from django.contrib.auth.admin import UserAdmin;

from front.models import Account;
from front.forms import CreateUserForm;

class AccountUserAdmin(UserAdmin):
    model = Account;
    add_form = CreateUserForm;
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Other info',
            {
                'fields': (
                    'address',
                )
            }
        )
    );


# Register your models here.
admin.site.register(Account, AccountUserAdmin);