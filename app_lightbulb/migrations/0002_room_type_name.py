# Generated by Django 5.1.5 on 2025-02-14 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_lightbulb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room_type',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
