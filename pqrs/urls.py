from django.urls import path

from .views import ManagePQRview, allPQRview, singlePQRview

app_name = "pqrs"
urlpatterns = [
    path("PQRS", allPQRview.as_view(), name="pqr"),
    path("PQRS/<int:pk>", singlePQRview.as_view(), name="pqr_get"),
    path("manage/PQRS/<int:pk>", ManagePQRview.as_view(), name="manage_pqr"),
]
