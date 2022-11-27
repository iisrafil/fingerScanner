from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from api.models import Device, Finger
from api.serializers import FingerSerializer
from scanner.models import Registered
from scanner.utility import scanner


class UploadViewSet(ViewSet):
    serializer_class = FingerSerializer

    def create(self, request):
        device = request.data.get('device')
        device = Device.objects.get(pk=device)
        file_uploaded = request.FILES.get('image')
        finger = Finger(device=device, image=file_uploaded)
        finger.save()
        result, time, percent = scanner(finger.image.path, device.depth);
        if percent > 60:
            user = Registered.objects.get(finger="Registered/" + result)
        else:
            return JsonResponse({
                "match": False,
                "finger": finger.pk,
            })
        return JsonResponse({
            "match": True,
            "user": user.id,
            "Name": user.name,
            "finger": result,
            "time": time,
        })