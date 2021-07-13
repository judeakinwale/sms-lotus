from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Faculty(models.Model):
    """Model definition for Faculty."""

    name = models.CharField(max_length=250, unique=True)
    code = models.IntegerField(null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    dean = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Faculty."""

        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculty')

    def __str__(self):
        """String representation of Faculty."""
        return self.name


class Department(models.Model):
    """Model definition for Department."""

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    code = models.CharField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Department."""

        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        """String representation of Department."""
        return self.name


class Programme(models.Model):
    """Model definition for Programme."""

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    code = models.CharField(max_length=250, null=True, blank=True, unique=True)
    max_level = models.ForeignKey("Level", on_delete=models.DO_NOTHING)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Programme."""

        verbose_name = _('Programme')
        verbose_name_plural = _('Programmes')

    def __str__(self):
        """String representation of Programme."""
        return self.name


class Course(models.Model):
    """Model definition for Course."""

    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    code = models.CharField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Course."""

        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __str__(self):
        """String representation of Course."""
        return self.name


class Level(models.Model):
    """Model definition for Level."""

    code = models.IntegerField(unique=True)

    class Meta:
        """Meta definition for Level."""

        verbose_name = _('Level')
        verbose_name_plural = _('Levels')

    def __str__(self):
        """String representation of Level"""
        return f'{self.code}'
