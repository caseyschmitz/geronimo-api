from django.db import models
from django.utils import timezone

class SpeedTest(models.Model):
    timestamp = models.DateTimeField(default=timezone.now, blank=False)
    data = models.CharField(max_length=256, blank=False)

    def __str__(self):
        return self.data