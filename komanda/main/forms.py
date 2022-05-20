from django import forms

from .models import Incomes

class IncomeEditForm(forms.ModelForm):

    class Meta:
        model = Incomes
        fields = ('value', 'name')

class IncomeAddForm(forms.ModelForm):

    class Meta:
        model = Incomes
        fields = ('value', 'name')