from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, View
from .models import RefundRequest
from .forms import RefundRequestForm
from django.conf import settings
import requests
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.cache import cache



class CreateRefundRequestView(LoginRequiredMixin, CreateView):
    model = RefundRequest
    form_class = RefundRequestForm
    template_name = 'refunds/create.html'
    success_url = reverse_lazy('refund_list')

    def get_initial(self):
        initial_data = {
            'order_number': '123456',
            'order_date': '2025-07-01',
            'first_name': 'Mikita',
            'last_name': 'Kashko',
            'phone_number': '+48883192530',
            'email': 'ivanov@example.com',
            'country': 'Poland',
            'address': 'Krakow, ul.Krakow',
            'postal_code': '30-555',
            'city': 'Krakow',
            'products': 'Товар 1, Товар 2',
            'reason': 'Некачественный товар',
            'bank_name': 'PKO',
            'account_type': 'private',
            'iban': 'PL12345678901234567890'
        }
        return initial_data

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RefundRequestListView(LoginRequiredMixin, ListView):
    model = RefundRequest
    template_name = 'refunds/list.html'
    context_object_name = 'refund_requests'
    
    def get_queryset(self):
        return RefundRequest.objects.filter(user=self.request.user).order_by('-created_at')


class RefundRequestDetailView(LoginRequiredMixin, DetailView):
    model = RefundRequest
    template_name = 'refunds/detail.html'
    context_object_name = 'refund_request'

class ValidateIBANView(View):
    def post(self, request):
        iban = request.POST.get('iban')
        if not iban:
            return JsonResponse({'error': 'IBAN не указан'}, status=400)

        cache_key = f'iban_validation_{iban}'
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return JsonResponse(cached_result)

        try:
            response = requests.get(
                'https://iban-validation.abstractapi.com/v1/',
                params={'api_key': "61766d918f364f1a8a05e2644e99f306", 'iban': iban}
            )
            response.raise_for_status()
            data = response.json()
            result = {
                'valid': data.get('is_valid', False),
                'message': 'IBAN действителен' if data.get('is_valid') else 'IBAN недействителен'
            }
            cache.set(cache_key, result, timeout=3600)
            return JsonResponse(result)
        except requests.RequestException as e:
            return JsonResponse({'error': f'Ошибка проверки IBAN: {str(e)}'}, status=500)