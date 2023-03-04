from django import forms

from goals.models import Goals, GoalExpense, GoalBump


class GoalAddForm(forms.ModelForm):
    class Meta:
        model = Goals
        fields = ("name", "start_date", "finish_date", "value")


class GoalAddExpenseForm(forms.ModelForm):
    class Meta:
        model = GoalExpense
        fields = ("date", "value")


class GoalBumpForm(forms.ModelForm):
    class Meta:
        model = GoalBump
        fields = ("date", "value")


class GoalEditForm(forms.ModelForm):
    class Meta:
        model = Goals
        fields = ("name", "start_date", "finish_date", "value")
