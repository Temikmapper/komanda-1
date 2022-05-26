from django import forms

from .models import Incomes, ConstantIncomes, ConstantIncomeHistory

class IncomeEditForm(forms.ModelForm):

    class Meta:
        model = Incomes
        fields = ('value', 'name')

class IncomeAddForm(forms.ModelForm):

    class Meta:
        model = Incomes
        fields = ('value', 'name')

class IncomeEditForm(forms.ModelForm):

    class Meta:
        model = ConstantIncomeHistory
        fields = ('value',)

class ConstantIncomeAddForm(forms.ModelForm):

    class Meta:
        model = ConstantIncomes
        fields = ('name', 'start_date')

class ConstantIncomeFinishForm(forms.ModelForm):

    class Meta:
        model = ConstantIncomes
        fields = ('finish_date', )