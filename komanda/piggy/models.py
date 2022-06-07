from decimal import Decimal
from django.db import models

class Piggies(models.Model):
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return f'/piggies/{self.id}'

    def get_current_value(self):
        try: 
            value = PiggyHistory.objects.filter(piggy=self).last().value
        except:
            value = Decimal(0.0)
        return value

    def get_history(self):
        
        return PiggyHistory.objects.filter(piggy=self)

    def get_capital(self):

        return PiggyHistory.objects.filter(piggy=self).aggregate(models.Sum('value'))['value__sum']

    def get_current_percent(self):

        try: 
            value = PiggyHistory.objects.filter(piggy=self).last().percent
        except:
            value = Decimal(0.0)
        return value

class PiggyHistory(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    percent = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    piggy = models.ForeignKey(Piggies, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']