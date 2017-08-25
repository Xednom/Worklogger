from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.
class Project(models.Model):
    project = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.project

class Time(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True)
    duration = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    remarks = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(("Date"), default=datetime.now())
