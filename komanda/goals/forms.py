from django import forms

from goals.models import Goals

class GoalAddForm(forms.ModelForm):

    class Meta:
        model = Goals
        fields = ('name', 'goal_date', 'goal_value')

class GoalEditForm(forms.ModelForm):

    class Meta:
        model = Goals
        fields = ('current_date', 'current_value')