from django.db import models
from django.contrib.postgres.fields import ArrayField


class SongMetadata(models.Model):
    title = models.CharField(max_length=200)
    contributors = ArrayField(models.CharField(max_length=100, blank=True))
    iswc = models.CharField(max_length=11)
    sources = ArrayField(models.CharField(max_length=100, blank=True))
    source_ids = ArrayField(models.IntegerField())

    def __str__(self):
        """Returns a string representation of a message."""
        return f"'{self.title}'"
