from django.db import models

class Piggies(models.Model):
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return f'/piggies/{self.id}'

    def get_current_value(self):
        try: 
            value = PiggyHistory.objects.filter(piggy=self).last().value
        except:
            value = 'Not stated'
        return value

class PiggyHistory(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)
    percent = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    piggy = models.ForeignKey(Piggies, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']