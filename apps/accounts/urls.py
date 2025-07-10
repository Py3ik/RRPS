from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    # PasswordResetDoneView,
    # PasswordResetConfirmView,
    # PasswordResetCompleteView,
)

from apps.accounts.views import SignUpView


urlpatterns = [
    path("login/", LoginView.as_view(next_page="/refunds"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/accounts/login/"), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    # path(
    #     "password_reset/done/",
    #     PasswordResetDoneView.as_view(
    #         template_name="registration/password_reset_done.html"
    #     ),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     PasswordResetConfirmView.as_view(
    #         template_name="registration/password_reset_confirm.html"
    #     ),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     PasswordResetCompleteView.as_view(
    #         template_name="registration/password_reset_complete.html"
    #     ),
    #     name="password_reset_complete",
    # ),
]