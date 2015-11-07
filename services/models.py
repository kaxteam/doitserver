from django.db import models
from django.utils import timezone


class Tracking(models.Model):
    starttime = models.DateTimeField(default=timezone.now)
    stoptime = models.DateTimeField(default=timezone.now)

class Path(models.Model):
    tracking = models.ForeignKey(Tracking)
    lat = models.FloatField()
    long = models.FloatField()
