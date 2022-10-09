from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from core.models import AbstractTimeStampedModel


class Station_132(AbstractTimeStampedModel):

    name = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    abbrevation = models.CharField(max_length=5)
    slug = models.SlugField(blank=True, null=True)
    station_type = models.CharField(max_length=3, default="132")
    image = models.ImageField(upload_to="stations_132/images")
    address = models.CharField(max_length=100, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    station_330 = models.ForeignKey("stations_330.Station_330", related_name="stations_132", on_delete=models.CASCADE)

    # GOOGLE SHEET RANGE

    acc_station_load = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = "132kV Station"
        verbose_name_plural = "132kV Stations"

    def __str__(self):
        return f"{self.name} 132kV TS"

    def get_absolute_url(self):
        return reverse("stations_132:detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("stations_132:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("stations_132:delete", kwargs={"slug": self.slug})

    def get_feeders_url(self):
        return reverse("feeders:list", kwargs={"slug": self.slug})

    def get_feeders_count(self):
        return self.feeders.count()

    def get_total_users(self):
        return self.users.count()

    def save(self, *args, **kwargs):
        self.name = str.capitalize(self.name)
        self.abbrevation = str.upper(self.abbrevation)
        self.slug = slugify(f"{self.name} 132")
        super(Station_132, self).save(*args, **kwargs)
