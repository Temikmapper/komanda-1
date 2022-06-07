from django import forms

from piggy.models import Piggies, PiggyHistory

class PiggyAddForm(forms.ModelForm):

    class Meta:
        model = Piggies
        fields = ('name',)

class PiggyBumpForm(forms.ModelForm):

    class Meta:
        model = PiggyHistory
        fields = ('date', 'value')

class PiggyEditForm(forms.ModelForm):

    class Meta:
        model = PiggyHistory
        fields = ('percent',)