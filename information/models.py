from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from academics import models as amodels

# Create your models here.


class Information(models.Model):
    """Model definition for Information."""

    source = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # limit_choices_to={'is_staff': True}
    )
    scope = models.ForeignKey("Scope", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Information."""

        verbose_name = _("Information")
        verbose_name_plural = _("Information")

    def __str__(self):
        """String representation of Information."""
        return f"{self.title} for {self.scope}"


class Notice(models.Model):
    """Model definition for Notice."""

    source  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scope = models.ForeignKey("Scope", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    message = models.TextField()

    class Meta:
        """Meta definition for Notice."""

        verbose_name = _("Notice")
        verbose_name_plural = _("Notices")

    def __str__(self):
        """String representation of Notice."""
        return self.title


class Scope(models.Model):
    """Model definition for Scope."""

    faculty = models.ForeignKey(amodels.Faculty, on_delete=models.CASCADE, null=True, blank=True)
    departmment = models.ForeignKey(amodels.Department, on_delete=models.CASCADE, null=True, blank=True)
    programme = models.ForeignKey(amodels.Programme, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(amodels.Course, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey(amodels.Level, on_delete=models.CASCADE, null=True, blank=True)

    description = models.CharField(max_length=250)
    is_general = models.BooleanField(default=True)
    is_first_year = models.BooleanField(default=False)
    is_final_year = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Scope."""

        verbose_name = _("Scope")
        verbose_name_plural = _("Scopes")

    def __str__(self):
        """String representation of Scope."""
        return self.description


class InformationImage(models.Model):
    """Model definition for InformationImage."""

    information = models.ForeignKey("Information", related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for InformationImage."""

        verbose_name = _("Information Image")
        verbose_name_plural = _("Information Images")

    def __str__(self):
        """String representation of InformationImage."""
        return self.description
