from django.db import models
from decimal import Decimal, ROUND_HALF_UP


class University(models.Model):
    PROGRAM_LEVELS = [
        ("D", "Diploma"),
        ("B", "Bachelor"),
        ("M", "Master"),
        ("P", "PhD"),
    ]

    university_name = models.CharField(max_length=200, unique=True)
    state = models.CharField(max_length=200)
    tuition_fees = models.DecimalField(max_digits=10, decimal_places=2)
    program_level = models.CharField(max_length=1, choices=PROGRAM_LEVELS)
    course_title = models.CharField(max_length=200)

    def __str__(self):
        return self.university_name
