from django.db import models

class UserData(models.Model):
    age = models.IntegerField()
    salary = models.FloatField()
    department = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)

class Rule(models.Model):
    rule = models.CharField(max_length=255, unique=True)  # Store the rule string

    def __str__(self):
        return self.rule

