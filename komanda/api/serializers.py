from rest_framework import serializers
from expenses.models import UsualExpenses, Categories


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            "id",
            "name",
        ]


class UsualExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsualExpenses
        fields = ["date", "amount", "category"]
