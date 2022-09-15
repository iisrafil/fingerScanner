from django.shortcuts import render

# Create your views here.

nav = ["home", "about", "owners", "vehicles"];

def front(req):
    context = {
        "nav": nav,
    }
    return render(req, "home.html", context);

def about(req):
    context = {
        "nav": nav,
    }
    return render(req, "about.html", context);

def owners(req):
    context = {
        "nav": nav,
    }
    return render(req, "owners.html", context);

def vehicles(req):
    context = {
        "nav": nav,
    }
    return render(req, "vehicles.html", context);