from django.contrib import admin
from django.urls import path, include
from . import views
from .dashboard import graphsPlot

urlpatterns = [
    path("", views.index, name="index"),
    path("form", views.form, name="compare"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path("admin", admin.site.urls),
    path('signup', views.signUp, name="signup"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("register", views.register_request, name="register"),
    path("compare", graphsPlot, name="compare")
]