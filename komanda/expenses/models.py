from datetime import date, timedelta
from tracemalloc import start
from django.db import models
from django.utils import timezone


class ConstantExpenseManager(models.Manager):
    def create(self, name, start_date, value):
        expense = super().create(
            name=name, start_date=start_date, finish_date=start_date + timedelta(730)
        )
        ConstantExpenseHistoryItem.objects.create(
            date=start_date, value=value, expense=expense
        )


class Categories(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class UsualExpenses(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f'Usual: {self.date} category "{self.category.name}" value {self.amount:.2f}'


class ConstantExpenses(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField(default=None)
    finish_date = models.DateField(default=None)
    objects = ConstantExpenseManager()

    def get_absolute_url(self):
        return f"/expenses/constant/{self.id}"

    def get_history(self):
        return ConstantExpenseHistoryItem.objects.filter(expense=self)


class ConstantExpenseHistoryItem(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    expense = models.ForeignKey(ConstantExpenses, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date"]
