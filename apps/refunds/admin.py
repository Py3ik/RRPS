from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from .models import RefundRequest


class RefundRequestResource(resources.ModelResource):
    class Meta:
        model = RefundRequest
        fields = (
            "id",
            "user__username",
            "order_number",
            "order_date",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "country",
            "address",
            "postal_code",
            "city",
            "products",
            "reason",
            "bank_name",
            "account_type",
            "iban",
            "iban_verified",
            "status",
            "created_at",
            "updated_at",
        )
        export_order = fields

    def get_export_headers(self, selected_fields=None):
        headers = [
            "ID",
            "User",
            "Order Number",
            "Order Date",
            "First Name",
            "Last Name",
            "Phone Number",
            "Email",
            "Country",
            "Address",
            "Postal Code",
            "City",
            "Products",
            "Reason",
            "Bank Name",
            "Account Type",
            "IBAN",
            "IBAN Verified",
            "Status",
            "Creation Date",
            "Update Date",
        ]

        if selected_fields:
            field_keys = list(self.fields.keys())
            return [
                headers[i]
                for i in range(len(headers))
                if field_keys[i] in selected_fields
            ]
        return headers

    def dehydrate_status(self, obj):
        return obj.get_status_display()

    def dehydrate_account_type(self, obj):
        return obj.get_account_type_display()


@admin.register(RefundRequest)
class RefundRequestAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = RefundRequestResource
    list_display = (
        "id",
        "order_number",
        "user",
        "status",
        "country",
        "created_at",
        "updated_at",
        "iban_verified",
    )
    list_filter = ("status", "created_at", "country")
    search_fields = ("order_number", "user__username", "email", "iban")
    list_per_page = 20
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("status",)
    autocomplete_fields = ["user"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
