from datetime import timedelta
from django.db import models


class ConstantIncomeManager(models.Manager):
    def create(self, name, start_date, value):
        income = super().create(
            name=name, start_date=start_date, finish_date=start_date + timedelta(730)
        )
        ConstantIncomeHistoryItem.objects.create(
            date=start_date, value=value, income=income
        )

class Incomes(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ConstantIncomes(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField(default=None)
    finish_date = models.DateField(default=None)
    objects = ConstantIncomeManager()

    def get_absolute_url(self):
        return f"/incomes/constant/{self.id}"

    def get_history(self):
        return ConstantIncomeHistoryItem.objects.filter(income=self)

    def bump(self, value, date):
        return ConstantIncomeHistoryItem.objects.create(
            date=date, value=value, income=self
        )

    def get_current_value(self):
        return ConstantIncomeHistoryItem.objects.filter(income=self).last().value


class ConstantIncomeHistoryItem(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    income = models.ForeignKey(ConstantIncomes, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date", "id"]
