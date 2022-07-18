from django.contrib import admin
from State import models
# Register your models here.

admin.site.register(models.CurrentState)
admin.site.register(models.Payment)
admin.site.register(models.SixMonthPayment)
admin.site.register(models.ThreeMonthPayment)