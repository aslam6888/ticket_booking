from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.admin)
admin.site.register(models.agent)
admin.site.register(models.trains)
admin.site.register(models.passenger)
admin.site.register(models.seat_booking)
admin.site.register(models.train_charts)
admin.site.register(models.booking_id)
admin.site.register(models.agent_booking_allowed)
