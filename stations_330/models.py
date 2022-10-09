from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from core.models import AbstractTimeStampedModel


class Station_330(AbstractTimeStampedModel):

    name = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    abbrevation = models.CharField(max_length=5)
    slug = models.SlugField(blank=True, null=True)
    station_type = models.CharField(max_length=3, default="330")
    image = models.ImageField(upload_to="stations_330/images")
    address = models.CharField(max_length=100, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "330kV Station"
        verbose_name_plural = "330kV Stations"

    def __str__(self):
        return f"{self.name} 330kV TS"

    def get_absolute_url(self):
        return reverse("stations_330:detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("stations_330:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("stations_330:delete", kwargs={"slug": self.slug})

    def get_total_users(self):
        return self.users.count()

    def get_total_132Stations(self):
        return self.stations_132.count()

    def save(self, *args, **kwargs):
        self.name = str.capitalize(self.name)
        self.slug = slugify(f"{self.name} 330")
        super(Station_330, self).save(*args, **kwargs)
