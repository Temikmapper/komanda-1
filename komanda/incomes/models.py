from django.db import models


class Incomes(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ConstantIncomes(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    finish_date = models.DateField()

    def get_absolute_url(self):
        return f"/incomes/constant/{self.id}"


class ConstantIncomeHistory(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    income = models.ForeignKey(ConstantIncomes, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date"]
