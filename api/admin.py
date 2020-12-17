from django.contrib import admin
from .models import SpeedTestClient, SpeedTest

admin.site.register(SpeedTestClient)
admin.site.register(SpeedTest)
