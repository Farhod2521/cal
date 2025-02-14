from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class  Type_of_premises(models.Model):
    title  =  models.CharField(max_length=300)
    lk = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return self.title
    




class Room_Type_Category(MPTTModel):  # MPTTModel dan meros olish
    name = models.CharField(max_length=1000)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_by = ["id"] # Kategoriyalar alfavit bo‘yicha tartiblanadi

    def __str__(self):
        return self.name


class Room_Type(models.Model):
    category = models.ForeignKey(Room_Type_Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, blank=True, null=True)
    lk = models.IntegerField()
    ra =  models.IntegerField()
    k =  models.IntegerField(verbose_name="Pulsatsiya", null=True, blank=True)
    table_height = models.FloatField(default=0.8, verbose_name="Ish stoli balandligi", null=True, blank=True)
    color_tem = models.CharField(max_length=200, null=True, blank=True)
    light_type   = models.CharField(max_length=200)
    recommended_lamps = models.CharField(max_length=200)


   
