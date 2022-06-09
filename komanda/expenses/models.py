from django.db import models
from django.utils import timezone


class Categories(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Expenses(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)


class ConstantExpenses(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    finish_date = models.DateField()

    def get_absolute_url(self):
        return f"/expenses/constant/{self.id}"

    def get_history(self):
        return ConstantExpenseHistory.objects.filter(expense=self)


class ConstantExpenseHistory(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    expense = models.ForeignKey(ConstantExpenses, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date"]
