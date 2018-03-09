from django.contrib import admin
from LogAdmin import models
admin.site.register(models.Host)
admin.site.register(models.Project)
admin.site.register(models.Application)
admin.site.register(models.AppType)