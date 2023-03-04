from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal
from django.db import models


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


class ConstantExpenses(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField(default=None)
    finish_date = models.DateField(default=None)
    objects = ConstantExpenseManager()

    class Meta:
        ordering = ["start_date", "id"]

    @staticmethod
    def get_objects_in_month(year: int, month: int):
        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)
        objects = ConstantExpenses.objects.filter(
            start_date__lte=first_date_in_month
        ).filter(finish_date__gte=last_date_in_month)

        return objects

    @staticmethod
    def get_sum_in_month(year: int, month: int):
        objects = ConstantExpenses.get_objects_in_month(year, month)
        result = Decimal(0)

        for item in objects:
            result += item.get_current_value()

        return result

    def get_value_in_month(self, year, month):
        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)

        # Если доход закончился, то возвращаем 0
        if last_date_in_month > self.finish_date:
            return 0

        history_items = ConstantExpenseHistoryItem.objects.filter(expense=self)
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

    def get_absolute_url(self):
        return f"/expenses/constant/{self.id}"

    def get_edit_url(self):
        return f"/expenses/constant/{self.id}/edit"

    def get_bump_url(self):
        return f"/expenses/constant/{self.id}/bump"

    def get_delete_url(self):
        return f"/expenses/constant/{self.id}/delete"

    def get_history(self):
        return ConstantExpenseHistoryItem.objects.filter(expense=self)

    def bump(self, value, date):
        return ConstantExpenseHistoryItem.objects.create(
            date=date, value=value, expense=self
        )

    def get_current_value(self):
        return ConstantExpenseHistoryItem.objects.filter(expense=self).last().value


class ConstantExpenseHistoryItem(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    expense = models.ForeignKey(ConstantExpenses, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date", "id"]
