from django.contrib import admin
from .models import Project, Time

# Register your models here.
class ProjectProfileAdmin(admin.ModelAdmin):
    list_display = ['project', 'description',]

class TimeProfileAdmin(admin.ModelAdmin):
    list_display = ['duration',]

admin.site.register(Project, ProjectProfileAdmin)
admin.site.register(Time, TimeProfileAdmin)
