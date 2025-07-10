from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

handler404 = "apps.refunds.views.page_not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("refunds/", include("apps.refunds.urls")),
]
