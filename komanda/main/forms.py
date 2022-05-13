from django import forms

from .models import Spendings, Categories

class SpendForm(forms.ModelForm):

    class Meta:
        model = Spendings
        fields = ('date', 'amount', 'category')

class CategoryAddForm(forms.ModelForm):

    class Meta:
        model = Categories
        fields = ('name',)