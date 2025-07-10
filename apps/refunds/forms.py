from django import forms
from .models import RefundRequest
from django.core.exceptions import ValidationError
import re

class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        exclude = ['user', 'status', 'iban_verified']

    def clean_iban(self):
        iban = self.cleaned_data.get('iban')
        print("IBAN:", iban)
        if not re.match(r'^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$', iban):
            raise ValidationError("Некорректный формат IBAN.")
        return iban