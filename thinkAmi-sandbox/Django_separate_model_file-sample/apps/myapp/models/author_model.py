from django.db import models
from .publication_model import Publication
from apps.outsideapp.models import Affiliation

class Author(models.Model):
    name = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)
    affiliations = models.ManyToManyField(Affiliation)