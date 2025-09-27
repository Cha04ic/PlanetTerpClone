from django.db import models

class Grade(models.Model):
    course = models.CharField(max_length=20)
    professor = models.CharField(max_length=50, null=True, blank=True)
    semester = models.IntegerField()
    section = models.CharField(max_length=10)
    a_plus = models.IntegerField()
    a = models.IntegerField()
    a_minus = models.IntegerField()
    b_plus = models.IntegerField()
    b = models.IntegerField()
    b_minus = models.IntegerField()
    c_plus = models.IntegerField()
    c = models.IntegerField()
    c_minus = models.IntegerField()
    d_plus = models.IntegerField()
    d = models.IntegerField()
    d_minus = models.IntegerField()
    f = models.IntegerField()
    w = models.IntegerField()
    other = models.IntegerField()



