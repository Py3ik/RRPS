from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, View
from .models import RefundRequest
from .forms import RefundRequestForm
from django.conf import settings
import requests
from django.http import JsonResponse
from django.core.cache import cache
from django.shortcuts import render


class CreateRefundRequestView(LoginRequiredMixin, CreateView):
    model = RefundRequest
    form_class = RefundRequestForm
    template_name = "refunds/create.html"
    success_url = reverse_lazy("refund_list")

    def get_initial(self):
        phone_number = (
            self.request.user.userprofile.phone_number
            if self.request.user.userprofile
            else ""
        )
        initial_data = {
            "order_number": "",
            "order_date": "",
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
            "phone_number": phone_number,
            "email": self.request.user.email,
            "country": "",
            "address": "",
            "postal_code": "",
            "city": "",
            "products": "",
            "reason": "",
            "bank_name": "",
            "account_type": "private",
            "iban": "",
        }
        return initial_data

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.iban_verified = True
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class RefundRequestListView(LoginRequiredMixin, ListView):
    model = RefundRequest
    template_name = "refunds/list.html"
    context_object_name = "refund_requests"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            RefundRequest.objects.select_related("user")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class RefundRequestDetailView(LoginRequiredMixin, DetailView):
    model = RefundRequest
    template_name = "refunds/detail.html"
    context_object_name = "refund_request"

    def get_queryset(self):
        return RefundRequest.objects.select_related("user").filter(
            user=self.request.user
        )


class ValidateIBANView(View):
    def post(self, request):
        iban = request.POST.get("iban")
        if not iban:
            return JsonResponse({"error": "IBAN is not provided"}, status=400)

        cache_key = f"iban_validation_{iban}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return JsonResponse(cached_result)

        try:
            response = requests.get(
                "https://ibanvalidation.abstractapi.com/v1/",
                params={"api_key": settings.ABSTRACT_API_KEY, "iban": iban},
            )
            response.raise_for_status()
            data = response.json()
            result = {
                "valid": data.get("is_valid", False),
                "message": (
                    "IBAN is valid"
                    if data.get("is_valid")
                    else "IBAN is invalid"
                ),
            }
            cache.set(cache_key, result, timeout=3600)
            return JsonResponse(result)
        except requests.RequestException as e:
            return JsonResponse(
                {"error": f"IBAN validation error: {str(e)}"}, status=500
            )


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
