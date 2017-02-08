from django.db import models

# Create your models here.

class Case(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    court = models.CharField(max_length=100)
    plaintiff = models.CharField(max_length=100)
    defendant = models.CharField(max_length=100)
    hashValue=models.CharField(max_length=100)
    prevHashValue=models.CharField(max_length=100)
    nonce=models.CharField(max_length=5)

class Verdict(models.Model):
    verdict_types = (
        ('in', 'intermediate'),
        ('end', 'end'),
    )
    #enum field mit End, Zwischen
    verdict_type=models.CharField(max_length=20,choices=verdict_types)
    text=models.CharField(max_length=1000)
    case=models.ForeignKey('Case')


class StatementOfFacts(models.Model):
    case=models.ForeignKey('Case')    

class Fact(models.Model):
    fact=models.CharField(max_length=1000)
    statementOfFacts=models.ForeignKey('StatementOfFacts')

class Consenus(models.Model):
    opinion=models.CharField(max_length=1000)
    statementOfFacts=models.ForeignKey('StatementOfFacts')


class View(models.Model):
    viewer_types = (
        ('pl', 'plaintiff'),
        ('df', 'defendant'),
    )
    viewer=models.CharField(max_length=20,choices=viewer_types)
    view=models.CharField(max_length=1000)
    statementOfFacts=models.ForeignKey('StatementOfFacts')



