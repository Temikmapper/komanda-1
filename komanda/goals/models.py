from datetime import datetime
from decimal import ROUND_FLOOR, Decimal
from django.db import models
from django.utils import timezone


class Goals(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    value = models.DecimalField(max_digits=13, decimal_places=2)
    accumulated = models.DecimalField(
        max_digits=13, decimal_places=2, default=Decimal(0)
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/goals/{self.id}/"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if len(GoalStatus.objects.filter(goal=self)) == 0:
            GoalStatus.objects.create(
                date=datetime.today(), value=Decimal(0), percent=Decimal(0), goal=self
            )

    def bump(self, value, date):
        self.accumulated += value
        self.save()
        return GoalStatus.objects.create(date=date, value=value, goal=self)

    def get_left(self):
        return (self.value - self.accumulated).quantize(Decimal("1.00"), ROUND_FLOOR)

    def get_percent(self):
        percent = (self.accumulated / self.value) * 100
        return percent.quantize(Decimal("1.00"), ROUND_FLOOR)

    def get_accumulated(self):
        return self.accumulated.quantize(Decimal("1.00"), ROUND_FLOOR)

    def get_history_list(self):
        statuses = GoalStatus.objects.filter(goal=self)
        return list(statuses)


class GoalStatus(models.Model):
    date = models.DateField(default=timezone.now)
    value = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal(0))
    percent = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal(0))
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date", "id"]

    def __str__(self) -> str:
        string = f"id: {self.id}, date: {self.date}"
        return string

    def left(self):

        return self.goal.value - self.value
