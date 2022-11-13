from calendar import monthrange
from datetime import date, datetime
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
        return f"/goals/{self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

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

    def get_value_in_month(self, year, month):
        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)
        history_items = GoalStatus.objects.filter(goal=self)
        before_month = history_items.filter(date__lte=last_date_in_month)
        after_month = history_items.filter(date__gte=first_date_in_month)
        objects_in_month = before_month & after_month
        try:
            if len(objects_in_month) == 0:
                value = 0
            else:
                value = objects_in_month.last().value
            return value
        except AttributeError:
            return 0


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
