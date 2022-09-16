from django.urls import path;
from . import views;

urlpatterns = [
    path("", views.front, name="home"),
    path("about/", views.about, name="about"),
    path("owners/", views.owners, name="owners"),
    path("vehicles/", views.vehicles, name="vehicles"),
    
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
];