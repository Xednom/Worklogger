from django.db import models
from datetime import datetime

# Create your models here.
class Project(models.Model):
    project = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.project + ' - ' + self.description

class Time(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True)
    duration = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    date = models.DateField(("Date"), default=datetime.now())
