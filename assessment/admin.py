from django.contrib import admin
from assessment import models

# Register your models here.

admin.site.register(models.Answer)
admin.site.register(models.Question)
admin.site.register(models.Quiz)
admin.site.register(models.QuizTaker)
admin.site.register(models.Response)
