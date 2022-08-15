from decimal import Decimal, ROUND_FLOOR
from django.db import models


class Piggies(models.Model):
    """Модель для свиньи-копилки
    """

    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return f"/piggies/{self.id}"

    def get_current_value(self):
        try:
            value = PiggyHistory.objects.filter(piggy=self).last().value
        except ValueError:
            value = Decimal(0.0)
        return value

    def get_history(self):

        return PiggyHistory.objects.filter(piggy=self)

    def get_capital(self):

        sum_of_bumps = PiggyHistory.objects.filter(piggy=self).aggregate(
            models.Sum("value")
        )["value__sum"]
        try:
            result = sum_of_bumps.quantize(Decimal("1.00"), ROUND_FLOOR)
        except AttributeError:
            result = Decimal(0)

        return result

    def get_current_percent(self):

        try:
            value = PiggyHistory.objects.filter(piggy=self).last().percent
        except ValueError:
            value = Decimal(0.0)
        return value

    def get_capital_till_date(self, date):

        try:
            sum_of_bumps = PiggyHistory.objects.filter(piggy=self).filter(
                date__lte=date
            )
            value = sum_of_bumps.aggregate(models.Sum("value"))["value__sum"].quantize(
                Decimal("1.00"), ROUND_FLOOR
            )
        except AttributeError:
            value = Decimal(0.0).quantize(Decimal("1.00"), ROUND_FLOOR)
        return value


class PiggyHistory(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    percent = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    piggy = models.ForeignKey(Piggies, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date"]
