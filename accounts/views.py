from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import CustomerRegistrationForm, ProfileUpdateForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard_redirect")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect("accounts:login")
        messages.error(request, "Please fix the errors below.")
    else:
        form = CustomerRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard_redirect")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("accounts:dashboard_redirect")
        messages.error(request, "Invalid username or password.")

    return render(
        request,
        "accounts/login.html",
        {"next": request.GET.get("next", "")},
    )


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


@login_required
def dashboard_redirect_view(request):
    if request.user.role == User.Role.ADMIN:
        return redirect("accounts:admin_dashboard")
    return redirect("accounts:customer_dashboard")


@login_required
def admin_dashboard_view(request):
    if request.user.role != User.Role.ADMIN:
        raise PermissionDenied("Admins only.")

    total_users = User.objects.count()
    customer_count = User.objects.filter(role=User.Role.CUSTOMER).count()
    return render(
        request,
        "accounts/admin_dashboard.html",
        {
            "total_users": total_users,
            "customer_count": customer_count,
        },
    )


@login_required
def customer_dashboard_view(request):
    if request.user.role != User.Role.CUSTOMER:
        raise PermissionDenied("Customers only.")

    return render(request, "accounts/customer_dashboard.html")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("accounts:profile")
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "profile_user": request.user,
        },
    )