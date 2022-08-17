from django import forms
from .models import (
    ConstantExpenses,
    ConstantExpenseHistoryItem,
    UsualExpenses,
    Categories,
)


class UsualExpenseAddForm(forms.ModelForm):
    class Meta:
        model = UsualExpenses
        fields = (
            "date",
            "amount",
            "category",
        )

class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ("name",)

class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ("name",)
        
class ConstExpenseEditForm(forms.ModelForm):
    class Meta:
        model = ConstantExpenses
        fields = ("name", "start_date", "finish_date")

class ConstExpenseAddForm(forms.Form):
    name = forms.CharField(max_length=50)
    start_date = forms.DateField()
    value = forms.DecimalField(max_digits=9, decimal_places=2)

class BumpExpenseForm(forms.ModelForm):
    class Meta:
        model = ConstantExpenseHistoryItem
        fields = ("date", "value")
