from django import forms
from .models import FreeMoney

class BumpFreeMoneyForm(forms.ModelForm):
    class Meta:
        model = FreeMoney
        fields = ("date", "value")