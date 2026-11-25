from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CurrencyConversionForm
from .models import CurrencyConversion


def _can_manage_record(user, record):
    return record.user == user or getattr(user, "role", None) == "ADMIN"


@login_required
def conversion_list(request):
    if getattr(request.user, "role", None) == "ADMIN":
        conversions = CurrencyConversion.objects.select_related("user").all()
    else:
        conversions = CurrencyConversion.objects.filter(user=request.user)

    total_php = conversions.aggregate(total=Sum("converted_php_amount"))["total"] or 0

    return render(
        request,
        "conversions/conversion_list.html",
        {
            "conversions": conversions,
            "total_php": total_php,
        },
    )


@login_required
def conversion_create(request):
    if request.method == "POST":
        form = CurrencyConversionForm(request.POST)
        if form.is_valid():
            conversion = form.save(commit=False)
            conversion.user = request.user
            conversion.save()
            messages.success(
                request,
                f"Converted {conversion.foreign_amount} {conversion.source_currency} "
                f"to ₱{conversion.converted_php_amount}.",
            )
            return redirect("conversions:list")
        messages.error(request, "Please fix the validation errors below.")
    else:
        form = CurrencyConversionForm()

    return render(
        request,
        "conversions/conversion_form.html",
        {"form": form, "action": "Create"},
    )


@login_required
def conversion_update(request, pk):
    conversion = get_object_or_404(CurrencyConversion, pk=pk)
    if not _can_manage_record(request.user, conversion):
        raise PermissionDenied("You do not have permission to edit this conversion.")

    if request.method == "POST":
        form = CurrencyConversionForm(request.POST, instance=conversion)
        if form.is_valid():
            updated = form.save()
            messages.success(
                request,
                f"Conversion updated: {updated.foreign_amount} {updated.source_currency} "
                f"= ₱{updated.converted_php_amount}.",
            )
            return redirect("conversions:list")
        messages.error(request, "Please fix the validation errors below.")
    else:
        form = CurrencyConversionForm(instance=conversion)

    return render(
        request,
        "conversions/conversion_form.html",
        {"form": form, "action": "Update", "conversion": conversion},
    )


@login_required
def conversion_delete(request, pk):
    conversion = get_object_or_404(CurrencyConversion, pk=pk)
    if not _can_manage_record(request.user, conversion):
        raise PermissionDenied("You do not have permission to delete this conversion.")

    if request.method == "POST":
        conversion.delete()
        messages.success(request, "Conversion record deleted.")
        return redirect("conversions:list")

    return render(
        request,
        "conversions/conversion_confirm_delete.html",
        {"conversion": conversion},
    )