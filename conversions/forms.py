from decimal import Decimal
from django import forms
from .models import CurrencyConversion


class CurrencyConversionForm(forms.ModelForm):
    class Meta:
        model = CurrencyConversion
        fields = [
            "source_currency",
            "foreign_amount",
            "exchange_rate_to_php",
            "purpose_note",
        ]
        widgets = {
            "source_currency": forms.Select(),
            "foreign_amount": forms.NumberInput(
                attrs={"step": "0.01", "min": "0.01", "placeholder": "e.g., 100.00"}
            ),
            "exchange_rate_to_php": forms.NumberInput(
                attrs={"step": "0.0001", "min": "0.0001", "placeholder": "e.g., 58.2500"}
            ),
            "purpose_note": forms.TextInput(
                attrs={"placeholder": "e.g., Family remittance or travel budget"}
            ),
        }

    def clean_foreign_amount(self):
        amount = self.cleaned_data.get("foreign_amount")
        if amount is None or amount <= Decimal("0"):
            raise forms.ValidationError("Foreign amount must be greater than zero.")
        if amount > Decimal("100000000.00"):
            raise forms.ValidationError("Amount exceeds the maximum allowed per transaction.")
        return amount

    def clean_exchange_rate_to_php(self):
        rate = self.cleaned_data.get("exchange_rate_to_php")
        if rate is None or rate <= Decimal("0"):
            raise forms.ValidationError("Exchange rate to PHP must be greater than zero.")
        return rate