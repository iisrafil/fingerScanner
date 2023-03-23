import os
from random import randint
from cv2 import split
from django.shortcuts import render, redirect;
from django.core.files.storage import FileSystemStorage;
from django.core.files.images import ImageFile;
from django.core.files.uploadedfile import UploadedFile;
from django.conf import settings;
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm;
from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import Group;
from django.contrib import messages;
from django.http import HttpRequest;
# from django.db.models.query import QuerySet;
# from django.http.request import QueryDict;
# from django.contrib.auth.mixins import
#  LoginRequiredMixin;
from .utils import get_chart, getUsers, matcher;
from .forms import *;
from .decorators import *;
from .models import *;
from api.models import Intruder;

import numpy as np;
import matplotlib.pyplot as plt;
import perfplot;
from time import time_ns as time;

# Create your views here.

nav = ["home", "simulation", "cam", "owners", "admins", "laws", "vehicles", "drivers"];


def call(*args, **kwargs):
    # perfplot.show(setup=np.random.rand, kernels=[np.sum,sum], n_range=[2**k for k in range(10)]);
    # sus = "./static/media/sus/1__M_Left_index_finger_CR.BMP";
    s = 100;
    try: s = int(args[0][0]);
    except: pass;
    if 0<s and s<=5288:
        cur = time();
        plt.imshow(matcher(s), origin="lower");
        print((time()-cur));
    else:
        tst_vals = [*range(1, 5288, 1000)];
        ts = [];
        for i in tst_vals:
            cur = time();
            matcher(i);
            ts.append(time()-cur);
        ts = [i/1e9 for i in ts];
        plt.plot(tst_vals, ts);
        plt.stem(tst_vals, ts);
    return;

def get_attrs(file):
    split_dunder = file.split("__");
    id = int(split_dunder[0]);

    split_under = split_dunder[1].split("_");
    finger = split_under[1][0].lower() + split_under[2][0];

    return (id, finger);

def init_load(req):
    messages.add_message(req, messages.INFO, "add driver fp");

    img_dir = "D:\\Baba\\SOCOFing\\Real\\".replace("\\", "/");
    pics = sorted(os.listdir(img_dir), key=lambda x: get_attrs(x)[0]);
    id_set = {get_attrs(x)[0] for x in pics};
    # print({x+1 for x in range(600)}-id_set);
    
    for i in id_set:
        Driver.objects.create(name=f"Driver-{i:03}", license_no=f"MHK{i:03}"+str(randint(100000000, 999999999)));
        pass;

    for file in pics:
        id, fin = get_attrs(file);
        try:
            d = Driver.objects.get(name=f"Driver-{id:03}");
            img = UploadedFile(file=open(img_dir+file, "rb"));
            Fingerprint.objects.create(of=d, finger=fin, img=img);
        except Exception as e: print(e);
    return {
        #
    };

def front(req: HttpRequest):
    if "pending" in str(req.user.groups.all()):
        messages.info(req, "Approval pending");
    context = {
        "nav": nav,
        # **init_load(req),
    };
    return render(req, "home.html", context);

chs = [
    ("cmp", "compare"),
    ("200", "200"),
    ("500", "500"),
];
class ChoiceForm(forms.Form):
    choices = forms.IntegerField(min_value=0, max_value=5288, label="Enter the size of search space (enter 0 to compare): ");

@login_required
@allowed_users(set())
def simulation(req: HttpRequest):
    form = ChoiceForm(req.POST or None);
    if form.is_valid():
        ss_val = form.cleaned_data.get("choices");
        return render(req, "about.html", {
            "nav": nav,
            "img": get_chart(call, ss_val),
            "form": form
        });
    context = {
        "nav": nav,
        "img": get_chart(call),
        "form": form
    };
    return render(req, "about.html", context);

@login_required
@allowed_users(set())
def rcv_pic(req: HttpRequest):
    users = Intruder.objects.all();

    context = {
        "nav": nav,
        "users": users,
    };
    return render(req, "cam.html", context);

@login_required(login_url="login")
@allowed_users({"law", "owner"})
def owners(req: HttpRequest):
    if "owner" in str(req.user.groups.all()):
        users = Account.objects.filter(groups__name__in=["owner", "pending_owner"], id=req.user.id);
    else: users = Account.objects.filter(groups__name__in=["owner", "pending_owner"]);
    
    context = {
        "nav": nav,
        "users": users,
    };
    return render(req, "owners.html", context);

@login_required
@allowed_users({"law", "owner"})
def owner(req: HttpRequest):
    pk = int(req.GET.get("pk"));
    if not (req.user.is_superuser or req.user.id == pk):
        messages.info(req, "Not your profile");
        return redirect("home");
    form = ProfileUpdateForm(initial=Account.objects.get(pk=pk).__dict__);
    if req.method == "POST":
        ac = Account.objects.get(pk=pk);
        form = ProfileUpdateForm(data=req.POST, instance=ac);
        if form.is_valid():
            form.save();
            messages.success(req, "Profile Updated");
            return redirect("owners");
    context = {
        "nav": nav,
        "form": form,
        "pk": pk,
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
@allowed_users(set())
def admin(req: HttpRequest):
    pk = int(req.GET.get("pk"));
    if req.user.id != pk:
        messages.info(req, "Not your profile");
        return redirect("home");
    form = ProfileUpdateForm(initial=Account.objects.get(pk=pk).__dict__);
    # print(form.data.keys())
    if req.method == "POST":
        ac = Account.objects.get(pk=pk);
        form = ProfileUpdateForm(data=req.POST, instance=ac);
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
    users = Account.objects.filter(groups__name__in=["law", "pending_law"]);
    
    context = {
        "nav": nav,
        "users": users,
    };
    return render(req, "laws.html", context);

@login_required
@allowed_users({"law"})
def law(req: HttpRequest):
    pk = int(req.GET.get("pk"));
    if not (req.user.is_superuser or req.user.id == pk):
        messages.info(req, "Not your profile");
        return redirect("home");
    form = ProfileUpdateForm(initial=Account.objects.get(pk=pk).__dict__);
    if req.method == "POST":
        ac = Account.objects.get(pk=pk);
        form = ProfileUpdateForm(data=req.POST, instance=ac);
        if form.is_valid():
            form.save();
            messages.success(req, "Profile Updated");
            return redirect("laws");
    context = {
        "nav": nav,
        "form": form,
        "pk": pk,
    };
    return render(req, "law.html", context);

@login_required
@allowed_users({"law", "owner"})
def vehicles(req: HttpRequest):
    vehicles = None;
    oid = req.GET.get("oid");
    did = req.GET.get("did");
    if "owner" in str(req.user.groups.all()):
        vehicles = Vehicle.objects.filter(owner__id=req.user.id);
    elif oid:
        vehicles = Vehicle.objects.filter(owner__id=oid);
    elif did:
        vehicles = Vehicle.objects.filter(driver__id=did);
    else:
        vehicles = Vehicle.objects.all();

    context = {
        "nav": nav,
        "vehicles": vehicles,
    };
    return render(req, "vehicles.html", context);

@login_required
@allowed_users({"owner"})
def vehicle(req: HttpRequest):
    oid = int(req.GET.get("oid"));
    if not (req.user.is_superuser or req.user.id == oid):
        messages.info(req, "Not your profile");
        return redirect("home");
    form = vid = cur_v = None;
    try:
        vid = int(req.GET.get("vid"));
        cur_v = Vehicle.objects.get(pk=vid);
        form = VehicleForm(instance=cur_v, initial={"owner": cur_v.owner});
    except:
        form = VehicleForm(initial={"owner": Account.objects.get(pk=oid)});
    if not req.user.is_superuser:
        form.fields["owner"].disabled = True;
    if req.method == "POST":
        mod_req = req.POST.copy();
        if not req.user.is_superuser:
            mod_req.update({"owner": req.user});
        form = VehicleForm(data=mod_req, instance=cur_v);
        if form.is_valid():
            form.save();
            messages.success(req, "Vehicle Added");
            return redirect("vehicles");
    context = {
        "nav": nav,
        "form": form,
        "pk": vid,
    };
    return render(req, "vehicle.html", context);

@login_required
@allowed_users({"law", "owner"})
def drivers(req: HttpRequest):
    pg_size = 15;
    page = req.GET.get("page");
    page = int(page) if page else 1;

    vid = req.GET.get("vid");
    if vid: drivers = Driver.objects.filter(vehicles__id=vid);
    elif "owner" in str(req.user.groups.all()):
        drivers = Driver.objects.filter(vehicles__owner__id=req.user.id);
    else: drivers = Driver.objects.all();

    n = drivers.count();
    mx = (n-1) // pg_size + 1;
    page = max(1, min(page, mx));
    start = (page-1) * pg_size;
    stop = start + pg_size;

    context = {
        "nav": nav,
        "drivers": drivers[start:stop],
        "page": page,
        "mx": mx,
    };
    return render(req, "drivers.html", context);

@login_required
@allowed_users({"owner"})
def add_vtod(req: HttpRequest):
    vid = req.GET.get("vid");
    form = AddDriverForm();

    if req.method == "POST":
        form = AddDriverForm(req.POST);
        ln = form.data["license_no"];
        try:
            d = Driver.objects.get(license_no=ln, approved=True);
            v = Vehicle.objects.get(pk=vid);
            d.vehicles.add(v);
            d.save();
        except Exception as e:
            messages.error(req, "Driver not found");
        return redirect("vehicles");

    context = {
        "nav": nav,
        "form": form,
        "vid": vid,
    }
    return render(req, "add_vtod.html", context);

@login_required
@allowed_users({"owner"})
def rm_vtod(req: HttpRequest):
    vid = req.GET.get("vid");
    drivers = Driver.objects.filter(vehicles__id=vid, approved=True);

    if req.method == "POST":
        new_dl = [];
        try: new_dl = req.POST.getlist("linked_drivers");
        except Exception as e:print(e);
        drvs = Driver.objects.filter(name__in=new_dl, approved=True);
        cur_v = Vehicle.objects.get(pk=vid);
        cur_v.driver_set.clear();
        cur_v.driver_set.add(*drvs.values_list("id", flat=True));
        cur_v.save();

        return redirect("vehicles");

    context = {
        "nav": nav,
        "vid": vid,
        "drivers": drivers,
    };
    return render(req, "rm_vtod.html", context);

@login_required
@allowed_users({"owner"})
def driver(req: HttpRequest):
    pk = req.GET.get("pk");
    form = DriverForm();
    if pk:
        if not (req.user.is_superuser or req.user.id in list(Account.objects.filter(vehicle__driver__id=pk).values_list("id", flat=True))):
            messages.info(req, "Not your profile");
            return redirect("home");
        form = DriverForm(initial=Driver.objects.get(pk=pk).__dict__);
    # except Exception as e: print(e);
    if req.method == "POST":
        form = DriverForm(data=req.POST);
        if form.is_valid():
            form.save();
            messages.success(req, "Profile Updated");
            return redirect("drivers");
    context = {
        "nav": nav,
        "form": form,
        "pk": pk,
    };
    return render(req, "driver.html", context);

@login_required
@allowed_users({"owner"})
def prints(req: HttpRequest):
    did = req.GET.get("did");
    driver = Driver.objects.get(pk=did);
    if req.method == 'POST':
        try:
            f = list(req.FILES.keys())[0].split(":")[1];
            fin = f.split("_");
            fin = fin[0][:1] + fin[1][:1];
            file = req.FILES["prints:"+f];
            Fingerprint.objects.create(of=driver, finger=fin, img=file);
        except Exception as e: print(e);
        response = redirect("prints");
        response["Location"] += "?did=" + did;
        return response;
    prints = [];
    for f, finger in Fingerprint.finger.field.choices:
        print_obj = None;
        try: print_obj = Fingerprint.objects.get(of=did, finger=f);
        except: pass;
        prints.append({
            "finger": finger,
            "print_obj": print_obj,
        });
    context = {
        "nav": nav,
        "driver": driver,
        "prints": prints,
    };
    return render(req, "prints.html", context);

@login_required
@allowed_users({"owner"})
def dtov(req: HttpRequest):
    action = req.GET.get("action");
    did = req.GET.get("did");
    if action == "rm":
        vehicles = Vehicle.objects.filter(driver__id=did, approved=True);
    else: 
        vehicles = Vehicle.objects.exclude(driver__id=did).exclude(approved=False);

    if req.method == "POST":
        new_vl = [];
        try: new_vl = req.POST.getlist("linked_vehicles");
        except Exception as e:print(e);
        new_vl = [int(s.split(":")[0]) for s in new_vl];
        cur_v = Vehicle.objects.get(pk=did);
        if action == "rm": cur_v.driver_set.clear();
        cur_v.driver_set.add(*new_vl);
        cur_v.save();

        return redirect("vehicles");

    context = {
        "nav": nav,
        "did": did,
        "vehicles": vehicles,
        "action": action,
    };
    return render(req, "dtov.html", context);

@login_required
@allowed_users({"owner"})
def delete(req: HttpRequest):
    type = req.GET.get("type");
    try:
        pk = int(req.GET.get("pk"));
        if type in ["admin", "owner", "law"]:
            tmp = Account.objects.get(pk=pk);
            tmp.delete();
        elif type == "driver":
            tmp = Driver.objects.get(pk=pk);
            tmp.delete();
        else: 
            tmp = Vehicle.objects.get(pk=pk);
            tmp.delete();
        messages.info(req, "Deleted :"+type);
    except Exception as e: 
        messages.error(req, "Delete error: "+str(e));
    return redirect(type+"s");

################# A U T H #######################

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
        else: messages.error(req, "Form not valid");

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
            grp = Group.objects.get(name="pending_"+form.data["type"]);
            user.groups.add(grp);
            messages.success(req, "successfully registered");
            return redirect("login");
    
    context = {
        "nav": nav,
        "form": form,
    };
    return render(req, "register.html", context);

@login_required
@allowed_users(set())
def approve(req: HttpRequest):
    tp = req.GET.get("type");
    try:
        if tp == "vehicle":
            v = Vehicle.objects.get(pk=req.GET.get("pk"));
            v.approved = True;
            v.save();
        elif tp == "driver":
            d = Driver.objects.get(pk=req.GET.get("pk"));
            d.approved = True;
            d.save();
        elif tp == "owner":
            o = Account.objects.get(pk=req.GET.get("pk"));
            o.groups.clear();
            o.groups.add(Group.objects.get(name="owner").id);
            o.approved = True;
            o.save();
        elif tp == "law":
            l = Account.objects.get(pk=req.GET.get("pk"));
            l.groups.clear();
            l.groups.add(Group.objects.get(name="law").id);
            l.approved = True;
            l.save();
    except Exception as e:
        if tp == "vehicle":
            Vehicle.objects.update(approved=True);
        elif tp == "driver":
            Driver.objects.update(approved=True);
        print(e);
    return redirect(tp+"s");