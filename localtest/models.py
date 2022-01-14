from django.db import models

# Create your models here.

class Panel(models.Model):
    _id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True)
    cur_test = models.CharField(max_length=20,blank=True)
    next_test = models.CharField(max_length=20,blank=True)
    _status = models.CharField(max_length=10,blank=True)
    _pass = models.PositiveIntegerField(default=0)
    _fail = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name_plural = "Panel"

class Percent(models.Model):
    percent = models.FloatField(default=0)
    _script = models.CharField(max_length=20,blank=True)
    class Meta:
        verbose_name_plural = "Percent"