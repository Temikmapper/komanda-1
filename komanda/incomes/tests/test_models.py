from datetime import date, datetime
from decimal import Decimal
from django.test import TestCase

from incomes.models import ConstantIncomeHistoryItem, ConstantIncomes, AdditionalIncomes


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

    def test_get_objects_in_month(self):
        income = ConstantIncomes.objects.get(name="phone")
        income.delete()
        ConstantIncomes.objects.create(
            name="2020-2022", start_date=date(2020, 1, 1), value=Decimal(100)
        )
        ConstantIncomes.objects.create(
            name="2021-2023", start_date=date(2021, 1, 1), value=Decimal(340)
        )
        ConstantIncomes.objects.create(
            name="2017-2019", start_date=date(2017, 1, 1), value=Decimal(270)
        )
        ConstantIncomes.objects.create(
            name="November'25", start_date=date(2025, 11, 15), value=Decimal(20000)
        )
        self.assertEqual(len(ConstantIncomes.get_objects_in_month(2021, 5)), 2)
        self.assertEqual(len(ConstantIncomes.get_objects_in_month(2022, 6)), 1)
        self.assertEqual(len(ConstantIncomes.get_objects_in_month(2023, 7)), 0)
        self.assertEqual(len(ConstantIncomes.get_objects_in_month(2025, 11)), 1)

    def test_sum_of_some_incomes(self):
        income = ConstantIncomes.objects.get(name="phone")
        income.delete()
        ConstantIncomes.objects.create(
            name="2020-2022", start_date=date(2020, 1, 1), value=Decimal(100)
        )
        ConstantIncomes.objects.create(
            name="2021-2023", start_date=date(2021, 1, 1), value=Decimal(340)
        )
        ConstantIncomes.objects.create(
            name="2017-2019", start_date=date(2017, 1, 1), value=Decimal(270)
        )
        self.assertEqual(ConstantIncomes.get_sum_in_month(2021, 5), Decimal(440))
        self.assertEqual(ConstantIncomes.get_sum_in_month(2022, 6), Decimal(340))
        self.assertEqual(ConstantIncomes.get_sum_in_month(2023, 7), Decimal(0))

    def test_has_actual_value_in_month(self):
        checked_income = ConstantIncomes.objects.create(
            name="November", start_date=date(2022, 11, 13), value=Decimal(20000)
        )
        november = ConstantIncomes.objects.get(name="November")
        november.bump(date=date(2022, 12, 1), value=Decimal(30000))
        self.assertEqual(november.get_value_in_month(2022, 11), Decimal(20000))
        self.assertEqual(november.get_value_in_month(2022, 12), Decimal(30000))


class AdditionalIncomesModelTest(TestCase):
    def test_get_objects_in_month(self):
        AdditionalIncomes.objects.create(
            name="1", value=Decimal(100), date=date(2022, 5, 5)
        )
        AdditionalIncomes.objects.create(
            name="2", value=Decimal(500), date=date(2022, 5, 7)
        )
        AdditionalIncomes.objects.create(
            name="3", value=Decimal(450), date=date(2022, 6, 5)
        )
        self.assertEqual(len(AdditionalIncomes.get_objects_in_month(2022, 5)), 2)
        self.assertEqual(len(AdditionalIncomes.get_objects_in_month(2022, 6)), 1)
        self.assertEqual(len(AdditionalIncomes.get_objects_in_month(2022, 7)), 0)

    def test_sum_of_some_incomes(self):
        AdditionalIncomes.objects.create(
            name="1", value=Decimal(100), date=date(2022, 5, 5)
        )
        AdditionalIncomes.objects.create(
            name="2", value=Decimal(500), date=date(2022, 5, 7)
        )
        AdditionalIncomes.objects.create(
            name="3", value=Decimal(450), date=date(2022, 6, 5)
        )
        self.assertEqual(AdditionalIncomes.get_sum_in_month(2022, 5), Decimal(600))
        self.assertEqual(AdditionalIncomes.get_sum_in_month(2022, 6), Decimal(450))
        self.assertEqual(AdditionalIncomes.get_sum_in_month(2022, 7), Decimal(0))
