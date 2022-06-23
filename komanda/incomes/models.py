from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal
from django.db import models


class ConstantIncomeManager(models.Manager):
    def create(self, name, start_date, value):
        income = super().create(
            name=name, start_date=start_date, finish_date=start_date + timedelta(730)
        )
        ConstantIncomeHistoryItem.objects.create(
            date=start_date, value=value, income=income
        )


class AdditionalIncomes(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    name = models.CharField(max_length=50)

    @staticmethod
    def get_objects_in_month(year: int, month: int):
        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)
        objects = AdditionalIncomes.objects.filter(
            date__gte=first_date_in_month
        ).filter(date__lte=last_date_in_month)
        return objects

    @staticmethod
    def get_sum_in_month(year: int, month: int):
        objects = AdditionalIncomes.get_objects_in_month(year, month)
        sum_ = objects.aggregate(models.Sum("value"))
        if sum_["value__sum"] == None:
            return Decimal(0.00)
        return sum_["value__sum"]

    def __str__(self):
        return self.name


class ConstantIncomes(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField(default=None)
    finish_date = models.DateField(default=None)
    objects = ConstantIncomeManager()

    @staticmethod
    def get_objects_in_month(year: int, month: int):
        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)
        objects = ConstantIncomes.objects.filter(
            start_date__lte=first_date_in_month
        ).filter(finish_date__gte=last_date_in_month)

        return objects

    @staticmethod
    def get_sum_in_month(year: int, month: int):
        objects = ConstantIncomes.get_objects_in_month(year, month)
        result = Decimal(0)

        for item in objects:
            result += item.get_current_value()

        return result

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
