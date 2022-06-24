from datetime import date
from decimal import Decimal
from django.db import models


class FreeMoney(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)

    class Meta:
        ordering = ["date", "id"]

    @staticmethod
    def bump(date, value):
        FreeMoney.objects.create(date=date, value=value)

    @staticmethod
    def get_value(year, month):
        objects = FreeMoney.objects.filter(date__lte=date(year, month, 1))
        if len(objects) == 0:
            return Decimal(0)
        return objects.last().value