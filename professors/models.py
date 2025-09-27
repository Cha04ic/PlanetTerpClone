from django.db import models

class Prof(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=30)
    type = models.CharField(max_length=20)
    courses = models.JSONField(default=list)
    avg_rating = models.FloatField(null=True, blank=True)

    def __str__(self):
      return f"{self.name}"
