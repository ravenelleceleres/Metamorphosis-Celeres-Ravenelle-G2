from django.contrib import admin
from .models import CurrencyConversion


@admin.register(CurrencyConversion)
class CurrencyConversionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "source_currency",
        "foreign_amount",
        "exchange_rate_to_php",
        "converted_php_amount",
        "created_at",
    )
    list_filter = ("source_currency", "created_at")
    search_fields = ("user__username", "purpose_note")