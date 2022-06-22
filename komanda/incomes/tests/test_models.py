from datetime import date, datetime
from decimal import Decimal
from django.test import TestCase

from incomes.models import (
    ConstantIncomeHistoryItem,
    ConstantIncomes,
)

class ConstIncomesModelTest(TestCase):
    def setUp(self):
        ConstantIncomes.objects.create(
            name="phone", start_date=date(2021, 1, 1), value=Decimal(100)
        )

    def test_const_income_creates_history_at_creation(self):
        income = ConstantIncomes.objects.get(name="phone")
        history_object = ConstantIncomeHistoryItem.objects.filter(income=income)
        self.assertEqual(len(history_object), 1)

    def test_returns_current_value(self):
        income = ConstantIncomes.objects.get(name="phone")
        income.bump(value=Decimal(200), date=date(2022, 1, 1))

        value = income.get_current_value()
        self.assertEqual(value, Decimal(200))
