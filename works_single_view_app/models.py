from django.db import models
from django.contrib.postgres.fields import ArrayField


class SongMetadata(models.Model):
    title = models.CharField(max_length=200, null=True)
    contributors = ArrayField(models.CharField(max_length=100, null=True))
    iswc = models.CharField(max_length=11, null=True, unique=False)
    sources = ArrayField(models.CharField(max_length=100, null=True))
    source_ids = ArrayField(models.IntegerField(null=True))

    def __str__(self):
        """Returns a string representation of a message."""
        return f"'{self.title}'"
