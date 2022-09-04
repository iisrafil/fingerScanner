from django.http import JsonResponse
from django.shortcuts import render

from scanner.utility import scanner

# Create your views here.
def home(request):
    result = scanner("Altered/Altered-Hard/150__M_Right_index_finger_Obl.BMP");
    return JsonResponse({"match": result})
