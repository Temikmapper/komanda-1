from django import forms

from .models import Incomes, Spendings, Categories

class SpendForm(forms.ModelForm):

    class Meta:
        model = Spendings
        fields = ('date', 'amount', 'category')

class CategoryAddForm(forms.ModelForm):

    class Meta:
        model = Categories
        fields = ('name',)

class IncomeEditForm(forms.ModelForm):

    class Meta:
        model = Incomes
        fields = ('value', 'name')

class IncomeAddForm(forms.ModelForm):

    class Meta:
        model = Incomes
        fields = ('value', 'name')