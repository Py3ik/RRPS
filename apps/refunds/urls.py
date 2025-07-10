from django.urls import path

from apps.refunds.views import (
    CreateRefundRequestView,
    RefundRequestListView,
    RefundRequestDetailView,
    ValidateIBANView,
)


urlpatterns = [
    path("", RefundRequestListView.as_view(), name="refund_list"),
    path("create/", CreateRefundRequestView.as_view(), name="create_refund"),
    path("<int:pk>/", RefundRequestDetailView.as_view(), name="refund_detail"),
    path("api/validate-iban/", ValidateIBANView.as_view(), name="validate_iban"),
]
