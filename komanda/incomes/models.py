from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal
from django.db import models

from main.mixin_models import BaseContinousEntity


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

    def get_current_value(self):
        return self.value

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
        if sum_["value__sum"] is None:
            return Decimal(0.00)
        return sum_["value__sum"]

    def __str__(self):
        return self.name


class ConstantIncomeHistoryItem(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    income = models.ForeignKey('ConstantIncomes', on_delete=models.CASCADE)

    class Meta:
        ordering = ["date", "id"]


class ConstantIncomes(models.Model, BaseContinousEntity):
    _name_class = "income"
    _url_name = "incomes"
    _child_class = ConstantIncomeHistoryItem
    name = models.CharField(max_length=50)
    start_date = models.DateField(default=None)
    finish_date = models.DateField(default=None)
    objects = ConstantIncomeManager()

    class Meta:
        ordering = ["name", "start_date"]

    @classmethod
    def get_objects_in_month(cls, year: int, month: int) -> models.QuerySet:
        """Получить все доходы за месяц

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            models.QuerySet: Queryset из доходов
        """
        return super().get_objects_in_month(year, month)

    @classmethod
    def get_sum_in_month(cls, year: int, month: int) -> Decimal:
        """Получить сумму доходов за месяц

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            Decimal: Сумма за месяц
        """ 
        return super().get_sum_in_month(year, month)

    def get_history(self) -> models.QuerySet:
        """Получить историю доходов

        Returns:
            models.QuerySet: Queryset из ConstantHistoryItem
        """
        return super().get_children()

    def bump(self, value: Decimal, date: date) -> ConstantIncomeHistoryItem:
        """Изменить значение ЗП

        Args:
            value (Decimal): Значение
            date (date): Дата изменения

        Returns:
            ConstantIncomeHistoryItem: Значение ЗП в моменте
        """
        return super().bump(value, date)

    def get_value_in_month(self, year: int, month: int) -> int:
        """Получить последнее значение дохода в определенном месяце

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            int: Значение
        """
        return super().get_value_in_month(year, month)

    def get_current_value(self) -> Decimal:
        return super().get_current_value()




