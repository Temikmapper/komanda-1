from datetime import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



class Goals(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    value = models.DecimalField(max_digits=13, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        GoalStatus.objects.create(date=datetime.today(), value=Decimal(0.0), percent=Decimal(0.0), goal=self)

    def __str__(self):
        return self.name


class GoalStatus(models.Model):
    date = models.DateField(default=timezone.now)
    value = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal(00.00))
    percent = models.DecimalField(
        max_digits=4, decimal_places=2, default=Decimal(00.00)
    )
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date"]

    def left(self):

        return self.goal.value - self.value