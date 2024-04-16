from django.urls import path

from .views import createPQRview, getPQRview

app_name = "pqrs"
urlpatterns = [
    path("PQRS", createPQRview.as_view(), name="pqr_create"),
    path("PQRS/<int:pk>", getPQRview.as_view(), name="pqr_get"),
    path("PQR/all", getPQRview.as_view(), name="pqr_get"),
]
