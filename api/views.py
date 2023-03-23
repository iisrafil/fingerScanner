from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest

from api.models import Device, Finger, Intruder
from api.serializers import FingerSerializer
from scanner.models import Registered
from scanner.utility import scanner, padd_bytes
from front.views import rcv_pic;

from django.core.files.base import ContentFile
from PIL import Image
import io

class UploadViewSet(ViewSet):
    serializer_class = FingerSerializer

    def create(self, request):
        device = request.data.get('device')
        device = Device.objects.get(pk=device)
        file_uploaded = request.FILES.get('image')
        byts = file_uploaded.file.getvalue();
        # print(byts)
        print(len(byts))
        byts = padd_bytes(byts);
        print(len(byts))
        img = Image.frombytes("L", (256, 288), byts);
        # img.show();
        buf = io.BytesIO();
        img.save(buf, format="BMP");
        buf.seek(0);
        finger = Finger(device=device, image=ContentFile(buf.read(), name="esp32-cam.bmp"))
        finger.save()
        reg = Registered(name="sami", finger=str(finger.image).split("/")[-1])
        reg.save();
        result, time, percent = scanner(finger.image.path);#, device.depth);
        if percent > 60:
            user = Registered.objects.get(finger=result)
        else:
            return JsonResponse({
                "match": False,
                "finger": finger.pk,
            }, safe=False)
        return JsonResponse({
            "match": True,
            "user": user.id,
            "Name": user.name,
            "finger": result,
            "time": time,
        }, safe=False)
    
@csrf_exempt
def cam(req: WSGIRequest):
    if req.method == "POST":
        ts = req.POST["timestamp"];
        dev_id = req.POST["id"];
        print(req.POST);
        byts = req.FILES.get("imageFile").file.getvalue();
        print(len(byts));
        # img = Image.frombytes("RGB", (320, 240), byts);
        img = Image.open(io.BytesIO(byts));
        # img.show();
        buf = io.BytesIO();
        img.save(buf, format="JPEG");
        buf.seek(0);
        dev = Device.objects.get(pk=dev_id);
        intruder = Intruder(device=dev, time=ts, image=ContentFile(buf.read(), name="intruder.jpeg"));
        intruder.save();
        return JsonResponse({"got_img": True}, safe=False);
    return rcv_pic(req);
