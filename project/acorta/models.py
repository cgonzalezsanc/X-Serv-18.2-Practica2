from django.db import models

# Create your models here.

class Url(models.Model):
    url_larga = models.CharField(max_length=32)
    url_corta = models.CharField(max_length=32)
