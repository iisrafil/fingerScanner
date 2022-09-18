from django.http import JsonResponse

from api.models import Device, Finger
from scanner.models import Registered
from scanner.utility import scanner


# Create your views here.
def home(request):
    device = Device.objects.get()
    finger = Finger.objects.get()

    result, time, percent = scanner(finger.image.path, device.depth);
    if percent:
        user = Registered.objects.get(finger="Registered/" + result)
    return JsonResponse({
        "user": user.id,
        "Name": user.name,
        "match": result,
        "time": time,
    })
