from django.db import models

class Affiliation(models.Model):
    name = models.CharField(max_length=50)