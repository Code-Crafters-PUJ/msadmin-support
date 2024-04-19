from django.urls import path

from .views import ManagePQRview, allPQRview, singleClientPQRview

app_name = "pqrs"
urlpatterns = [
    path("PQRS", allPQRview.as_view(), name="pqr"),
    path("PQRS/<int:pk>", singleClientPQRview.as_view(), name="pqr_client"),
    path("PQRS/<int:pk>/manage", ManagePQRview.as_view(), name="manage_pqr"),
]
