from django import forms
from .models import Expenses, Categories


class AddExpenseForm(forms.ModelForm):

    class Meta:
        model = Expenses
        fields = ('date', 'amount', 'category')

class CategoryAddForm(forms.ModelForm):

    class Meta:
        model = Categories
        fields = ('name',)