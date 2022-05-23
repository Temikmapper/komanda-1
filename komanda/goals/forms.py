from django import forms

from goals.models import Goals, GoalStatus

class GoalAddForm(forms.ModelForm):

    class Meta:
        model = Goals
        fields = ('name', 'date', 'value')

class GoalStatusAddForm(forms.ModelForm):

    class Meta:
        model = GoalStatus
        fields = ('date', 'value')