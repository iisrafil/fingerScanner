from urllib import request
from django.shortcuts import render, redirect;
from front.utils import getUsers;
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm;
from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import Group;
from django.contrib import messages;
from django.db.models.query import QuerySet;
from django.http import HttpRequest;
# from django.contrib.auth.mixins import LoginRequiredMixin;
from .forms import CreateUserForm, ProfileUpdateForm;
from .decorators import authenticated_already, allowed_users;
from .utils import get_chart;
from .models import Account;

# Create your views here.

nav = ["home", "about", "owners", "admins", "laws", "vehicles"];

def front(req: HttpRequest):
    context = {
        "nav": nav,
        "img": get_chart(),
    };
    return render(req, "home.html", context);

def about(req: HttpRequest):
    context = {
        "nav": nav,
    };
    return render(req, "about.html", context);

@login_required(login_url="login")
@allowed_users({"law", "owner"})
def owners(req: HttpRequest):
    users = Account.objects.filter(groups__name__in=["owner"]);
    
    context = {
        "nav": nav,
        "users": users,
    };
    return render(req, "owners.html", context);

@login_required
@allowed_users({"law", "owner"})
def owner(req: HttpRequest):
    pk = int(req.GET.get("pk"));
    if req.user.id != pk:
        messages.info(req, "Not your profile");
        return redirect("home");
    form = ProfileUpdateForm(instance=req.user);
    if req.method == "POST":
        form = ProfileUpdateForm(data=req.POST, instance=req.user);
        if form.is_valid():
            form.save();
            messages.success(req, "Profile Updated");
            return redirect("owners");
    context = {
        "nav": nav,
        "form": form,
    };
    return render(req, "owner.html", context);

@login_required(login_url="login")
@allowed_users({"law"})
def admins(req: HttpRequest):
    users = Account.objects.filter(groups__isnull=True);
    
    context = {
        "nav": nav,
        "users": users,
    };
    return render(req, "admins.html", context);

@login_required
@allowed_users({"law"})
def admin(req: HttpRequest):
    pk = int(req.GET.get("pk"));
    if req.user.id != pk:
        messages.info(req, "Not your profile");
        return redirect("home");
    form = ProfileUpdateForm(instance=req.user);
    if req.method == "POST":
        form = ProfileUpdateForm(data=req.POST, instance=req.user);
        if form.is_valid():
            form.save();
            messages.success(req, "Profile Updated");
            return redirect("admins");
    context = {
        "nav": nav,
        "form": form,
    };
    return render(req, "admin.html", context);

@login_required(login_url="login")
@allowed_users({"law"})
def laws(req: HttpRequest):
    users = Account.objects.filter(groups__name__in=["law"]);
    
    context = {
        "nav": nav,
        "users": users,
    };
    return render(req, "laws.html", context);

@login_required
@allowed_users({"law"})
def law(req: HttpRequest):
    pk = int(req.GET.get("pk"));
    if req.user.id != pk:
        messages.info(req, "Not your profile");
        return redirect("home");
    form = ProfileUpdateForm(instance=req.user);
    if req.method == "POST":
        form = ProfileUpdateForm(data=req.POST, instance=req.user);
        if form.is_valid():
            form.save();
            messages.success(req, "Profile Updated");
            return redirect("laws");
    context = {
        "nav": nav,
        "form": form,
    };
    return render(req, "law.html", context);

def vehicles(req: HttpRequest):
    context = {
        "nav": nav,
    };
    return render(req, "vehicles.html", context);

@authenticated_already
def login_view(req: HttpRequest):
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
def logout_view(req: HttpRequest):
    logout(req);
    return redirect("home");

@authenticated_already
def register_view(req: HttpRequest):
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
    };
    return render(req, "register.html", context);