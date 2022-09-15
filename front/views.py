from django.shortcuts import render

# Create your views here.

def front(req):
    return render(req, "home.html", {});