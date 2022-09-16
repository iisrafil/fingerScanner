from django.shortcuts import render, redirect;
from front.utils import getUsers;
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm;
from django.contrib.auth.decorators import login_required;
# from django.contrib.auth.mixins import LoginRequiredMixin;

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

@login_required
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

def login_view(req):
    err = None;
    form = AuthenticationForm();
    if req.method == "POST":
        form = AuthenticationForm(data=req.POST);
        if form.is_valid():
            username = form.cleaned_data.get("username");
            password = form.cleaned_data.get("password");
            user = authenticate(username=username, password=password);
            if user is not None:
                login(req, user);
                if req.GET.get("next"):
                    return redirect(req.GET.get("next"));
                else: return redirect("home");
        else: err = "From not valid";

    context = {
        "nav": nav,
        "form": form,
        "err": err,
    };
    return render(req, "login.html", context);
def logout_view(req):
    logout(req);
    return redirect("home");