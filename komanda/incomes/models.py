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
        before_month = ConstantIncomes.objects.filter(
            start_date__lte=last_date_in_month
        )
        after_month = ConstantIncomes.objects.filter(
            finish_date__gte=first_date_in_month
        )
        objects = before_month & after_month
        return objects

    @staticmethod
    def get_sum_in_month(year: int, month: int):
        objects = ConstantIncomes.get_objects_in_month(year, month)
        result = Decimal(0)

        for item in objects:
            result += item.get_value_in_month(year, month)

        return result

    def get_absolute_url(self):
        return f"/incomes/constant/{self.id}"

    def get_edit_url(self):
        return f"/incomes/constant/{self.id}/edit"

    def get_bump_url(self):
        return f"/incomes/constant/{self.id}/bump"

    def get_delete_url(self):
        return f"/incomes/constant/{self.id}/delete"

    def get_history(self):
        return ConstantIncomeHistoryItem.objects.filter(income=self)

    def bump(self, value, date):
        return ConstantIncomeHistoryItem.objects.create(
            date=date, value=value, income=self
        )

    def get_value_in_month(self, year: int, month: int) -> int:
        """Получить доходы в месяце

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            int: Значение
        """
        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)

        # Если доход закончился, то возвращаем 0
        if (last_date_in_month > self.finish_date):
            return 0

        history_items = ConstantIncomeHistoryItem.objects.filter(income=self)
        before_month = history_items.filter(date__lte=last_date_in_month)
        after_month = history_items.filter(date__gte=first_date_in_month)
        objects_in_month = before_month & after_month
        try:
            if len(objects_in_month) == 0:
                value = before_month.last().value
            else:
                value = objects_in_month.last().value
            return value
        except AttributeError:
            return 0

    def get_current_value(self):
        return ConstantIncomeHistoryItem.objects.filter(income=self).last().value


class ConstantIncomeHistoryItem(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    income = models.ForeignKey(ConstantIncomes, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date", "id"]
