from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal
from django.db import models

from main.mixin_models import BaseContinousEntity


class ConstantExpenseManager(models.Manager):
    def create(self, name, start_date, value):
        expense = super().create(
            name=name, start_date=start_date, finish_date=start_date + timedelta(730)
        )
        ConstantExpenseHistoryItem.objects.create(
            date=start_date, value=value, expense=expense
        )


class Categories(models.Model):
    colors = [
        ("hsl(169, 75.4%, 41.4%)", "Бирюзовый"),
        ("hsl(140, 44.8%, 51%)", "Зелёный"),
        ("hsl(203,64.9%,52%)", "Синий"),
        ("hsl(203,67.9%,43.9%)", "Тёмно-синий"),
        ("hsl(289,29.1%,50.2%)", "Пурпуный"),
        ("hsl(210,28.8%,28.6%)", "Тёмно-серый"),
        ("hsl(48,88%,51%)", "Жёлтый"),
        ("hsl(35,91.5%,54.1%)", "Оранжевый"),
        ("hsl(28,80.3%,52.2%)", "Тёмно-оранжевый"),
        ("hsl(5,78.8%,57.5%)", "Красный"),
        ("hsl(6,63%,46.7%)", "Тёмно-красный"),
        ("hsl(213,9.1%,76.3%)", "Светло-серый"),
    ]
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=50, choices=colors, default="hsl(6,63%,46.7%)")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/expenses/categories/{self.id}"

    def get_edit_url(self):
        return f"/expenses/categories/{self.id}/edit"


class UsualExpenses(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    @staticmethod
    def get_objects_in_month(year: int, month: int):
        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)
        objects = UsualExpenses.objects.filter(date__gte=first_date_in_month).filter(
            date__lte=last_date_in_month
        )

        return objects

    @staticmethod
    def get_sum_in_month(year: int, month: int):
        objects = UsualExpenses.get_objects_in_month(year, month)

        sum_ = objects.aggregate(models.Sum("amount"))
        if sum_["amount__sum"] is None:
            return Decimal(0.00)
        return sum_["amount__sum"]

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f'Usual: {self.date} category "{self.category.name}" value {self.amount:.2f}'


class ConstantExpenseHistoryItem(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    expense = models.ForeignKey("ConstantExpenses", on_delete=models.CASCADE)

    class Meta:
        ordering = ["date", "id"]


class ConstantExpenses(models.Model, BaseContinousEntity):
    _name_class = "expense"
    _url_name = "expenses"
    _child_class = ConstantExpenseHistoryItem
    name = models.CharField(max_length=50)
    start_date = models.DateField(default=None)
    finish_date = models.DateField(default=None)
    objects = ConstantExpenseManager()

    class Meta:
        ordering = ["name", "start_date"]

    @classmethod
    def get_objects_in_month(cls, year: int, month: int) -> models.QuerySet:
        return super().get_objects_in_month(year, month)

    @classmethod
    def get_sum_in_month(cls, year: int, month: int) -> Decimal:
        return super().get_sum_in_month(year, month)

    def get_value_in_month(self, year: int, month: int) -> Decimal:
        return super().get_value_in_month(year, month)

    def get_history(self) -> models.QuerySet:
        return super().get_children()

    def bump(self, value: Decimal, date: date) -> models.Model:
        return super().bump(value, date)

    def get_current_value(self) -> Decimal:
        return super().get_current_value()
