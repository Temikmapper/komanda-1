from django.db import models

class Incomes(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name