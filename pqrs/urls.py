from django.urls import path

from .views import allPQRview, singlePQRview

app_name = "pqrs"
urlpatterns = [
    path("PQRS", allPQRview.as_view(), name="pqr"),
    path("PQRS/<int:pk>", singlePQRview.as_view(), name="pqr_get"),
]
