from django.db import models

class Course(models.Model):
    department = models.TextField()
    course_number = models.CharField(max_length=10)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    credits = models.IntegerField(null=True, blank=True)
    average_gpa = models.FloatField(null=True, blank=True)
    is_recent = models.BooleanField(default=True)
    name = models.TextField(unique=True)
    professors = models.JSONField(default=list)


    def __str__(self):
        return f"{self.name}"
