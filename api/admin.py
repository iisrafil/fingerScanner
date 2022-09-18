from django.contrib import admin

from api.models import Device, Intruder, Data, Finger

# Register your models here.


admin.site.register(Finger)
admin.site.register(Device)
admin.site.register(Intruder)
admin.site.register(Data)
