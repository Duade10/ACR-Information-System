from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import DetailView, FormView, UpdateView

from . import forms, mixins, models


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        username = email.split("@")[0]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            return redirect(reverse("users:login"))
        return super().form_valid(form)

    def get_success_url(self):
        url = self.request.META.get("HTTP_REFERER")
        # try:
        #     query = requests.utils.urlparse(url).query
        #     params = dict(x.split('=')for x in query.split('&'))
        #     if 'next' in params:
        #         nextPage = params['next']
        #         return redirect(nextPage)
        next_arg = self.request.GET.get("next")
        messages.success(self.request, f"Welcome {self.request.user.first_name}")
        if next_arg is not None:
            return redirect(next_arg)
        else:
            return reverse("core:home")


def log_out(request):
    logout(request)
    messages.success(request, "See you later")
    return redirect(reverse("users:login"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        username = email.split("@")[0]
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            user.is_active = False
            user.verify_email(self.request)
        return redirect("/users/login/?command=verification&email=" + email)


class UserUpdateView(UpdateView):
    model = models.User
    template_name = "users/edit_user.html"
    form_class = forms.UpdateForm

    def form_valid(self, form):
        data = form.save()
        return redirect(data.get_absolute_url())


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # todo: Add Messages
        # messages.success(request, "Email Verification Activation Successfull")
    return redirect("core:home")


class UserDetailView(mixins.LoggedInOnlyView, DetailView):
    model = models.User
    template_name = "users/user_profile.html"
    context_object_name = "single_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_protection_guarantees = self.get_object().protection_guarantees.count()
        total_trouble_reports = self.get_object().trouble_reports.count()
        context["total_protection_guarantees"] = total_protection_guarantees
        context["total_trouble_reports"] = total_trouble_reports
        return context


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        if models.User.objects.filter(email=email).exists():
            user = models.User.objects.get(email__exact=email)
            user.send_reset_email(request)
            messages.success(request, "Password reset email has been sent to your email address.")
            return redirect("users:login")

        else:
            messages.error(request, "Account does not exist")
            return redirect("users:forgot_password")

    return render(request, "users/forgot_password.html")


def validate_reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your Password")
        return redirect("users:reset_password")
    else:
        messages.error(request, "This reset link has expired.")
        return redirect("users:reset_password")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Password do not match")
            return redirect("users:reset_password")
        else:
            uid = request.session.get("uid")
            user = models.User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("users:login")
    else:
        return render(request, "users/reset_password.html")
