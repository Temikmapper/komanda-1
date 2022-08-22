from django import forms

from .models import AdditionalIncomes, ConstantIncomes, ConstantIncomeHistoryItem


class IncomeEditForm(forms.ModelForm):
    class Meta:
        model = AdditionalIncomes
        fields = ("value", "name")


class IncomeAddForm(forms.ModelForm):
    class Meta:
        model = AdditionalIncomes
        fields = ("value", "name")


# class IncomeEditForm(forms.ModelForm):
#     class Meta:
#         model = ConstantIncomeHistoryItem
#         fields = ("value",)


class ConstIncomeAddForm(forms.ModelForm):
    class Meta:
        model = ConstantIncomes
        fields = ("name", "start_date")


class ConstantIncomeAddForm(forms.Form):
    name = forms.CharField(max_length=50)
    start_date = forms.DateField()
    value = forms.DecimalField(max_digits=9, decimal_places=2)


class ConstantIncomeFinishForm(forms.ModelForm):
    class Meta:
        model = ConstantIncomes
        fields = ("finish_date",)


class ConstantIncomeEditForm(forms.ModelForm):
    class Meta:
        model = ConstantIncomes
        fields = ("name", "start_date", "finish_date")


class BumpIncomeForm(forms.ModelForm):
    class Meta:
        model = ConstantIncomeHistoryItem
        fields = ("date", "value")
