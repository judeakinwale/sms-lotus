from django.contrib import admin
from information import models

# Register your models here.

admin.site.register(models.Information)
admin.site.register(models.InformationImage)
admin.site.register(models.Notice)
admin.site.register(models.Scope)
