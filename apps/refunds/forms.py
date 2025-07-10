from django import forms
from django.core.cache import cache
from django.core.exceptions import ValidationError
import re
import requests
from django.conf import settings
from .models import RefundRequest
from django.forms.widgets import DateInput


class RefundRequestForm(forms.ModelForm):
    order_date = forms.DateField(
        widget=DateInput(attrs={"type": "date"}), required=True
    )

    class Meta:
        model = RefundRequest
        exclude = ["user", "status", "iban_verified"]

    def clean_iban(self):
        iban = self.cleaned_data.get("iban")

        if not re.match(r"^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$", iban):
            raise ValidationError("Некорректный формат IBAN.")

        cache_key = f"iban_validation_{iban}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            if not cached_result["valid"]:
                raise ValidationError("IBAN недействителен (по данным кэша).")
            return iban
        try:
            response = requests.get(
                "https://ibanvalidation.abstractapi.com/v1/",
                params={"api_key": settings.ABSTRACT_API_KEY, "iban": iban},
            )
            response.raise_for_status()
            data = response.json()

            is_valid = data.get("is_valid", False)
            if not is_valid:
                cache.set(cache_key, {"valid": False}, timeout=3600)
                raise ValidationError("IBAN недействителен.")

            cache.set(cache_key, {"valid": is_valid}, timeout=3600)
            return iban

        except requests.RequestException as e:
            raise ValidationError("Ошибка проверки IBAN. Попробуйте позже.")
