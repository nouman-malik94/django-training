import datetime

from django.db import models


# Create your models here.
class CatCity(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class CatTrainingType(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Training(models.Model):
    name = models.CharField(max_length=255, default='training')
    type = models.ForeignKey(CatTrainingType, on_delete=models.CASCADE, default=1)
    date_start = models.DateField(default=datetime.date.today)
    date_end = models.DateField(default=datetime.date.today)
    city = models.ForeignKey(CatCity, on_delete=models.CASCADE, default=1)
    street_address = models.CharField(max_length=255, default='Islamabad')

class TrainingFile(models.Model):
    fk_training = models.ForeignKey(Training, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    file = models.FileField(blank=True, upload_to='training/')

    def __str__(self):
        return self.description

class ResourceItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    estimated_price = models.IntegerField()
    fk_training = models.ForeignKey(Training, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ResourcePerson(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    pin = models.CharField(max_length=6)
    father_name = models.CharField(max_length=255)
    cnic = models.CharField(max_length=13)
    fk_training = models.ForeignKey(Training, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
