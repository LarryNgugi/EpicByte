from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home", views.index, name="index"),
    path("form", views.form, name="compare"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path("admin", admin.site.urls),
    path('signup', views.signUp, name="signup")
]