from django import forms
from .models import ConstantExpenses, ConstantExpenseHistory, Expenses, Categories


class AddExpenseForm(forms.ModelForm):

    class Meta:
        model = Expenses
        fields = ('date', 'amount', 'category',)

class CategoryAddForm(forms.ModelForm):

    class Meta:
        model = Categories
        fields = ('name',)

class ExpenseEditForm(forms.ModelForm):

    class Meta:
        model = ConstantExpenseHistory
        fields = ('value',)

class ConstantExpenseAddForm(forms.ModelForm):

    class Meta:
        model = ConstantExpenses
        fields = ('name', 'start_date')

class ConstantExpenseFinishForm(forms.ModelForm):

    class Meta:
        model = ConstantExpenses
        fields = ('finish_date', )