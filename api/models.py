from django.db import models
from django.utils import timezone

def default_scheduled():
    return timezone.now() + timezone.timedelta(minutes=5)

class TestNode(models.Model):
    '''A node that Tests can be executed from.'''

    name = models.CharField(max_length=128, unique=True, blank=False)
    uri = models.URLField(unique=True, blank=False)
    active = models.BooleanField(default=True, blank=False)

    # to appease pylint
    objects = models.Manager()

    def __str__(self):
        return '{}({})'.format(self.name, self.uri)


class SpeedTest(models.Model):
    '''A test to get the speed an latency of a network.'''

    class Type(models.IntegerChoices):
        TEST = 0
        ADHOC = 1
        SCHEDULED = 2

    type = models.IntegerField(default=0, choices=Type.choices, blank=False)
    owner = models.ForeignKey('auth.User', related_name='speedtests', on_delete=models.CASCADE)
    node = models.ForeignKey(TestNode, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=timezone.now, editable=False, blank=False)
    scheduled = models.DateTimeField(default=default_scheduled, blank=False)
    started = models.DateTimeField(editable=False, null=True, blank=True)
    completed = models.DateTimeField(editable=False, null=True, blank=True)
    data = models.CharField(editable=False, max_length=256, blank=True)

    # to appease pylint
    objects = models.Manager()

    #def save(self, *args, **kwargs):
    #    pass

    #def __str__(self):
    #    return self.id
