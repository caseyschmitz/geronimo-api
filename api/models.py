from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

PORTPATTERN = '([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])'
IPPATTERN = rf'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\:{PORTPATTERN})?$'
HOSTPATTERN = rf'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])(\:{PORTPATTERN})?$'

def default_scheduled():
    return timezone.now() + timezone.timedelta(minutes=5)

def HostValidator(host):
    ipmatch = re.fullmatch(IPPATTERN, host)
    hostmatch = re.fullmatch(HOSTPATTERN, host)

    if ipmatch is None and hostmatch is None:
        raise ValidationError(
            _('%(host)s is not a valid host.'),
            code='invalid',
            params={'host': host},
        )

class SpeedTestClient(models.Model):
    '''A node that Tests can be executed from.'''

    name = models.CharField(max_length=128, unique=True, blank=False)
    uri = models.URLField(unique=True, blank=False)
    active = models.BooleanField(default=True, blank=False)

    # to appease pylint
    objects = models.Manager()

    def __str__(self):
        return '{}({})'.format(self.name, self.uri)


class SpeedTestServer(models.Model):

    # the maximum length of a domain name is 253 characters - add 6 for port designation
    host = models.CharField(max_length=259, validators=[HostValidator], blank=False)
    server_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=256, blank=False)
    sponsor = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=64, blank=True)
    country_code = models.CharField(max_length=10, blank=True)
    # distance is measured in kilometers
    distance_km = models.DecimalField(max_digits=10, decimal_places=5, editable=False)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, editable=False)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, editable=False)

    # to appease pylint
    objects = models.Manager()

class SpeedTestResult(models.Model):

    #speedtest = models.OneToOneField('SpeedTest', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(editable=False, blank=False)
    server = models.OneToOneField(SpeedTestServer, on_delete=models.CASCADE)
    ping = models.DecimalField(default=0.0, max_digits=16, decimal_places=4, editable=False, blank=False)
    bytes_received = models.IntegerField(default=0, editable=False, blank=False)
    bytes_sent = models.IntegerField(default=0, editable=False, blank=False)
    download_bytes = models.DecimalField(default=0.0, max_digits=16, decimal_places=4, editable=False, blank=False)
    upload_bytes = models.DecimalField(default=0.0, max_digits=16, decimal_places=4, editable=False, blank=False)
    image_url = models.URLField(editable=False, blank=False)

    # to appease pylint
    objects = models.Manager()


class SpeedTest(models.Model):
    '''A test to get the speed an latency of a network.'''

    class Type(models.IntegerChoices):
        TEST = 0
        ADHOC = 1
        SCHEDULED = 2

    type = models.IntegerField(default=0, choices=Type.choices, blank=False)
    owner = models.ForeignKey('auth.User', related_name='speedtests', on_delete=models.CASCADE)
    client = models.ForeignKey(SpeedTestClient, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=timezone.now, editable=False, blank=False)
    scheduled = models.DateTimeField(default=default_scheduled, blank=False)
    started = models.DateTimeField(editable=False, null=True, blank=True)
    completed = models.DateTimeField(editable=False, null=True, blank=True)
    result = models.OneToOneField(SpeedTestResult, on_delete=models.CASCADE, editable=False, blank=True)

    # to appease pylint
    objects = models.Manager()

    #def save(self, *args, **kwargs):
    #    pass

    #def __str__(self):
    #    return self.id
