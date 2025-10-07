from django.db import models

# Create your models here.
class Savol(models.Model):
    BOLIM_CHOICES = [
        ('tashqi_muhit', 'Tashqi Muhit Qulayligi va Sifati'),
        ('arxitektura', 'Arxitektura Sifati va Obyektlarning Joylashuvi'),
        ('ichki_muhit', 'Ichki Muhit Ekologiyasi va Qulayligi'),
        ('sanitariya', 'Salomatlikni Muhofaza Qilish va Chiqindilarni Yo\'q Qilish'),
        ('suv', 'Suvdan Oqilona Foydalanish'),
        ('energiya', 'Energiya Tejamkorlik va Energiya Samaradorlik'),
        ('qayta_tiklanadigan', 'Muqobil va Qayta Tiklanadigan Energiya Manbalari'),
        ('ekologiya', 'Ob\'ektlarni Yarati, Ishla va Foydalanish Ekologiyasi'),
        ('iqtisodiy', 'Iqtisodiy Samaradorlik'),
        ('loyihalash', 'Loyihani Tayyorlash va Boshqarish Sifati'),
    ]
    
    SAVOL_TURI_CHOICES = [
        ('number', 'Raqamli'),
        ('select', 'Tanlov'),
        ('checkbox', 'Checkbox'),
        ('text', 'Matn'),
    ]
    
    raqam = models.IntegerField()
    nom = models.TextField()
    bolim = models.CharField(max_length=50, choices=BOLIM_CHOICES)
    savol_turi = models.CharField(max_length=20, choices=SAVOL_TURI_CHOICES)
    maksimal_ball = models.IntegerField()
    izoh = models.TextField(blank=True, null=True)
    tartib = models.IntegerField(default=0)
    faol = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['bolim', 'tartib', 'raqam']
        unique_together = ['bolim', 'raqam']
    
    def __str__(self):
        return f"{self.raqam}. {self.nom}"

class BallQoidasi(models.Model):
    savol = models.ForeignKey(Savol, on_delete=models.CASCADE, related_name='ball_qoidalari')
    shart = models.CharField(max_length=100, help_text="Masalan: <=200, yoki 'ha'")
    ball = models.IntegerField()
    izoh = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['savol', 'ball']
    
    def __str__(self):
        return f"{self.savol.raqam}: {self.shart} -> {self.ball} ball"

class TanlovVariant(models.Model):
    savol = models.ForeignKey(Savol, on_delete=models.CASCADE, related_name='tanlov_variantlari')
    qiymat = models.CharField(max_length=100)
    ball = models.IntegerField()
    tartib = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['savol', 'tartib']
    
    def __str__(self):
        return f"{self.savol.raqam}: {self.qiymat}"