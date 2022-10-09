from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("logout/", views.log_out, name="logout"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("sign-up/", views.SignUpView.as_view(), name="sign_up"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("update/<int:pk>", views.UserUpdateView.as_view(), name="update"),
    path("profile/<int:pk>/", views.UserDetailView.as_view(), name="profile"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path(
        "validate-reset-password/<uidb64>/<token>/",
        views.validate_reset_password,
        name="validate_reset_password",
    ),
]
