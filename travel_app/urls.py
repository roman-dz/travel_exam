from django.urls import path
from .import views


urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("addtrip", views.create_first),
    path("travel", views.all_plans),
    path("travel/new", views.create_first),
    path("travel/create", views.create_plan),
    path("travel/<int:plan_id>", views.one_plan),
    path("addtrip/<int:plan_id>/update", views.update),
    path("travel/<int:plan_id>/delete", views.delete),
    path("joined/<int:plan_id>", views.joined),
    path("unjoined/<int:plan_id>", views.unjoined),
    path("logout", views.logout),
]