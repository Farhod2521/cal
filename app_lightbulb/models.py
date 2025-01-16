from django.db import models

class  Type_of_premises(models.Model):
    title  =  models.CharField(max_length=300)
    lk = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return self.title
    


