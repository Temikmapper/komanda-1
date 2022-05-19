from decimal import Decimal
from tkinter import CASCADE
from django.db import models
from django.utils import timezone


class Goals(models.Model):
    name = models.CharField(max_length=50)
    current_date = models.DateField(default=timezone.now)
    current_value = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal(00.00))
    current_percent = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal(00.00))
    goal_date = models.DateField()
    goal_value = models.DecimalField(max_digits=13, decimal_places=2)

    def left(self):
        return self.goal_value - self.current_value

    def __str__(self):
        return self.name
