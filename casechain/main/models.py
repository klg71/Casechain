from django.db import models

# Create your models here.

class Case(models.Model):
    hashValue=models.CharField(max_length=100)
    prevHashValue=models.CharField(max_length=100)
    nonce=models.CharField(max_length=5)

class Text(models.Model):
    textType=models.CharField("max_length=10")
    part=models.IntegerField()
    case=models.ForeignKey('Case')
    text=models.CharField(max_length=1000)

#class Verdict(models.Model):

