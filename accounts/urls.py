from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_redirect_view, name="dashboard_redirect"),
    path("dashboard/admin/", views.admin_dashboard_view, name="admin_dashboard"),
    path("dashboard/customer/", views.customer_dashboard_view, name="customer_dashboard"),
    path("profile/", views.profile_view, name="profile"),
]