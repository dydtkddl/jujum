from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
  path("home", home),
  path("signup",signup),
  path("register",register),
  path("main",main),
  path("signout", signout),
  path("rerole", rerole),
  path("register_order",register_order),
  path("register_serve_complete",register_serve_complete),
  path("render",render_),
  path("get_not_served", get_not_served),
  path("get_served", get_served),
  path("register_order", register_order),
  path("reception_withdraw", reception_withdraw),
  path("deleteReception", deleteReception),
  path("get_not_cook", get_not_cook),
  path("cookOccupy", cookOccupy),
]