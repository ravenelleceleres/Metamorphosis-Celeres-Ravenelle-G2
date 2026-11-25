from django.urls import path
from . import views

app_name = "conversions"

urlpatterns = [
    path("", views.conversion_list, name="list"),
    path("new/", views.conversion_create, name="create"),
    path("<int:pk>/edit/", views.conversion_update, name="update"),
    path("<int:pk>/delete/", views.conversion_delete, name="delete"),
]