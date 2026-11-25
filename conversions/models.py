from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class CurrencyConversion(models.Model):
    class Currency(models.TextChoices):
        USD = "USD", "US Dollar (USD)"
        EUR = "EUR", "Euro (EUR)"
        GBP = "GBP", "British Pound (GBP)"
        JPY = "JPY", "Japanese Yen (JPY)"
        AUD = "AUD", "Australian Dollar (AUD)"
        SGD = "SGD", "Singapore Dollar (SGD)"
        CAD = "CAD", "Canadian Dollar (CAD)"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="currency_conversions",
    )
    source_currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.USD,
    )
    foreign_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    exchange_rate_to_php = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0001"))],
    )
    converted_php_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        editable=False,
    )
    purpose_note = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.converted_php_amount = (
            self.foreign_amount * self.exchange_rate_to_php
        ).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.user.username}: {self.foreign_amount} {self.source_currency} "
            f"= ₱{self.converted_php_amount}"
        )