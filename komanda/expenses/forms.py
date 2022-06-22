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


class ConstExpenseEditForm(forms.ModelForm):
    class Meta:
        model = ConstantExpenses
        fields = ("name", "start_date", "finish_date")


class ConstExpenseAddForm(forms.ModelForm):
    class Meta:
        model = ConstantExpenses
        fields = ("name", "start_date")


class ConstExpenseHistoryAddForm(forms.ModelForm):
    """Поле для ввода значения траты, используется только при инициализации постоянной траты"""

    class Meta:
        model = ConstantExpenseHistoryItem
        fields = ("value",)


class BumpExpenseForm(forms.ModelForm):
    class Meta:
        model = ConstantExpenseHistoryItem
        fields = ("date", "value")
