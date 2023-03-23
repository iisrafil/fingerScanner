from django.urls import path;
from . import views;

urlpatterns = [
    path("", views.front, name="home"),
    path("simulation/", views.simulation, name="simulation"),
    path("cam/", views.rcv_pic, name="cam"),
    path("owners/", views.owners, name="owners"),
    path("owner/", views.owner, name="owner"),
    path("admins/", views.admins, name="admins"),
    path("admin/", views.admin, name="admin"),
    path("laws/", views.laws, name="laws"),
    path("law/", views.law, name="law"),
    path("vehicles/", views.vehicles, name="vehicles"),
    path("vehicle/", views.vehicle, name="vehicle"),
    path("drivers/", views.drivers, name="drivers"),
    path("add_vtod/", views.add_vtod, name="add_vtod"),
    path("rm_vtod/", views.rm_vtod, name="rm_vtod"),
    path("driver/", views.driver, name="driver"),
    path("prints/", views.prints, name="prints"),
    path("dtov/", views.dtov, name="dtov"),

    path("approve/", views.approve, name="approve"),

    path("delete/", views.delete, name="delete"),
    
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
];