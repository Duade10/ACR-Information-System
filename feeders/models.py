from core.models import AbstractTimeStampedModel
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Feeder(AbstractTimeStampedModel):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=20, unique=True, null=True, blank=True)
    station_132 = models.ForeignKey("stations_132.Station_132", related_name="feeders", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} 33kV"

    def get_absolute_url(self):
        return reverse("feeders:detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("feeders:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("feeders:delete", kwargs={"station_slug": self.station_132.slug, "pk": self.pk})

    def save(self, *args, **kwargs):
        self.name = str.capitalize(self.name)
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
