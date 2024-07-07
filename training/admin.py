from django.contrib import admin
from . import models

admin.site.register(models.CatCity)
admin.site.register(models.CatTrainingType)
admin.site.register(models.TrainingFile)
admin.site.register(models.ResourcePerson)
admin.site.register(models.ResourceItem)
admin.site.register(models.Training)
