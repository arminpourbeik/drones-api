from django.contrib import admin

from drones import models

admin.site.register(models.DroneCategory)
admin.site.register(models.Drone)
admin.site.register(models.Pilot)
admin.site.register(models.Competition)
