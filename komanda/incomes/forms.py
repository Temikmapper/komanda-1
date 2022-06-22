from django import forms

from .models import Incomes, ConstantIncomes, ConstantIncomeHistoryItem


class IncomeEditForm(forms.ModelForm):
    class Meta:
        model = Incomes
        fields = ("value", "name")


class IncomeAddForm(forms.ModelForm):
    class Meta:
        model = Incomes
        fields = ("value", "name")


class IncomeEditForm(forms.ModelForm):
    class Meta:
        model = ConstantIncomeHistoryItem
        fields = ("value",)


class ConstIncomeAddForm(forms.ModelForm):
    class Meta:
        model = ConstantIncomes
        fields = ("name", "start_date")


class ConstantIncomeFinishForm(forms.ModelForm):
    class Meta:
        model = ConstantIncomes
        fields = ("finish_date",)

class ConstIncomeHistoryAddForm(forms.ModelForm):
    """Поле для ввода значения траты, используется только при инициализации постоянного дохода"""

    class Meta:
        model = ConstantIncomeHistoryItem
        fields = ("value",)

class ConstIncomeEditForm(forms.ModelForm):
    class Meta:
        model = ConstantIncomes
        fields = ("name", "start_date", "finish_date")

class BumpIncomeForm(forms.ModelForm):
    class Meta:
        model = ConstantIncomeHistoryItem
        fields = ("date", "value")