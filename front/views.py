from django.shortcuts import render, redirect;
from front.utils import getUsers;
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm;
from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import Group;
from django.contrib import messages;
# from django.contrib.auth.mixins import LoginRequiredMixin;
from .forms import CreateUserForm;
from .decorators import authenticated_already, allowed_users;
from .utils import get_chart;

# Create your views here.

nav = ["home", "about", "owners", "vehicles"];

def front(req):
    context = {
        "nav": nav,
        "img": get_chart(),
    }
    return render(req, "home.html", context);

def about(req):
    context = {
        "nav": nav,
    }
    return render(req, "about.html", context);

@login_required(login_url="login")
@allowed_users({"law"})
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

@authenticated_already
def login_view(req):
    form = AuthenticationForm();
    if req.method == "POST":
        form = AuthenticationForm(data=req.POST);
        if form.is_valid():
            username = form.cleaned_data.get("username");
            password = form.cleaned_data.get("password");
            user = authenticate(username=username, password=password);
            if user is not None:
                login(req, user);
                messages.success(req, "login successful " + user.get_username());
                if req.GET.get("next"):
                    return redirect(req.GET.get("next"));
                else: return redirect("home");
        else: messages.error(req, "From not valid");

    context = {
        "nav": nav,
        "form": form,
    };
    return render(req, "login.html", context);
def logout_view(req):
    logout(req);
    return redirect("home");

@authenticated_already
def register_view(req):
    form = CreateUserForm();
    if req.method == "POST":
        form = CreateUserForm(data=req.POST);
        if form.is_valid():
            user = form.save();
            grp = Group.objects.get(name="owner");
            user.groups.add(grp);
            messages.success(req, "successfully registered");
            return redirect("login");
    
    context = {
        "nav": nav,
        "form": form,
    }
    return render(req, "register.html", context);