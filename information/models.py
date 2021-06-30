from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Information(models.Model):

    source = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True}
    )
    scope = models.ForeignKey("Scope", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Information")
        verbose_name_plural = _("Information")

    def __str__(self):
        return f"{self.title} for {self.scope}"


class Notice(models.Model):

    source  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    scope = models.ForeignKey("Scope", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    message = models.TextField()

    class Meta:
        verbose_name = _("Notice")
        verbose_name_plural = _("Notices")

    def __str__(self):
        return self.title


class Scope(models.Model):

    # TODO:
    # faculty
    # departmment
    # course
    # programme
    # level
    description = models.CharField(max_length=250)
    is_general = models.BooleanField(default=True)
    is_first_year = models.BooleanField(default=False)
    is_final_year = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Scope")
        verbose_name_plural = _("Scopes")

    def __str__(self):
        return self.description


class InformationImage(models.Model):

    information = models.ForeignKey("Information", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/%Y/%m/%d", max_length=None)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Information Image")
        verbose_name_plural = _("Information Images")

    def __str__(self):
        return self.description
