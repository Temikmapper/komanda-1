from django import forms
from .models import ConstantExpenses, ConstantExpenseHistory, UsualExpenses, Categories


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


class ConstantExpenseEditForm(forms.ModelForm):
    class Meta:
        model = ConstantExpenseHistory
        fields = ("value",)


class ConstantExpenseAddForm(forms.ModelForm):
    class Meta:
        model = ConstantExpenses
        fields = ("name", "start_date")


class ConstantExpenseFinishForm(forms.ModelForm):
    class Meta:
        model = ConstantExpenses
        fields = ("finish_date",)
