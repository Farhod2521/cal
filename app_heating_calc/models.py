from django.db import models

# Create your models here.


class Region(models.Model):
    name = models.CharField(max_length=200)

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    average_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
