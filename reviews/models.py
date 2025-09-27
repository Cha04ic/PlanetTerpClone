from django.db import models
from courses.models import Course
from professors.models import Prof
from django.contrib.auth.models import User


GRADE_CHOICES = [
    ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
    ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
    ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
    ('D+', 'D+'), ('D', 'D'), ('D-', 'D-'),
    ('F', 'F'),
    ('W', 'W'),     # Withdrawal
    ('P', 'P'),     # Pass
    ('XF', 'XF'),   # Failure due to academic dishonesty
]


class Review(models.Model):
    professor = models.ForeignKey(Prof, on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, null=True, blank=True)
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.professor.name} - {self.course.name} ({self.rating} stars)"


