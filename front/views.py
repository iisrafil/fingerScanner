from django.shortcuts import render
from front.utils import getUsers;

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
    data = getUsers()["data"];
    # data = [{"a": 1}];
    users = [list(data[0].keys())];
    users += [list(user.values()) for user in data];
    context = {
        "nav": nav,
        "users": users,
    }
    return render(req, "owners.html", context);

def vehicles(req):
    context = {
        "nav": nav,
    }
    return render(req, "vehicles.html", context);