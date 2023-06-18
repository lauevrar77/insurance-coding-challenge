from django.urls import path

from quotes import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quote/submit", views.submit_quote, name="submit_quote"),
    path(
        "quote/<uuid:simulation_uuid>/result", views.quote_result, name="quote_result"
    ),
]
