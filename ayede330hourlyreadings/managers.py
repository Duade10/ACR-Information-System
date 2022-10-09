from django.utils import timezone
from django.db import models
from django.db.models import Q


class MaximumReadingError(Exception):
    """This error class is raised when a Hourly Reading Sheet has 24 Hourly Readings"""

    pass


class CustomReadingManager(models.Manager):
    def get_count_or_create(self, **kwargs):
        try:
            obj = self.get(**kwargs)
            if obj.hourly_readings.count() == 24:
                raise MaximumReadingError()
            else:
                return obj
        except AttributeError:
            obj = self.get(
                Q(created_at__day=timezone.now().day)
                & Q(created_at__month=timezone.now().month)
                & Q(created_at__year=timezone.now().year)
            )
            if obj.hourly_reading.count() == 24:
                raise MaximumReadingError()
            else:
                return obj
        except obj.DoesNotExist:
            if obj.objects.last().hourly_readings.count < 24:
                return obj.objects.last()
            else:
                raise MaximumReadingError()
        except MaximumReadingError():
            return obj.objects.create(created_at=timezone.now())
