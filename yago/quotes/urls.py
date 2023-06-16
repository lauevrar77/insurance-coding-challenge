from django.urls import path

from quotes import views

urlpatterns = [
    path("", views.index, name="index"),
]
