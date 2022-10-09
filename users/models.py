from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator

# Account Verification Imports
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode


class User(AbstractUser):
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    STATION_330 = "330"
    STATION_132 = "132"

    DESIGNATION_CHOICES = (
        (STATION_330, "330kV"),
        (STATION_132, "132kV"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=24, blank=True)
    supervisor = models.BooleanField(default=False)
    designation = models.CharField(choices=DESIGNATION_CHOICES, max_length=4, null=True)
    station_330 = models.ForeignKey(
        "stations_330.Station_330",
        related_name="users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    station_132 = models.ForeignKey(
        "stations_132.Station_132",
        related_name="users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.first_name = str.capitalize(self.first_name)
        self.last_name = str.capitalize(self.last_name)
        super().save(*args, **kwargs)

    def get_full_name(self) -> str:
        return super().get_full_name()

    def get_station(self):
        if self.designation == "132":
            return self.station_132
        else:
            return self.station_330

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self, request):
        current_site = get_current_site(request)
        domain = current_site
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)

        html_message = render_to_string(
            "email/user_verification_email.html",
            {"domain": domain, "uidb64": uid, "token": token, "first_name": self.first_name},
        )
        send_mail(
            "Activate your Account",
            strip_tags(html_message),
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
            html_message=html_message,
        )
        self.save()

    def send_reset_email(self, request):
        current_site = get_current_site(request)
        domain = current_site
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)

        html_message = render_to_string(
            "email/reset_password_email.html",
            {"domain": domain, "uidb64": uid, "token": token, "first_name": self.first_name},
        )
        send_mail(
            "Reset Your Password",
            strip_tags(html_message),
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
            html_message=html_message,
        )
