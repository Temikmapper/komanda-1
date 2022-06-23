from datetime import date
from decimal import Decimal
from django.test import TestCase

from expenses.models import (
    Categories,
    UsualExpenses,
    ConstantExpenseHistoryItem,
    ConstantExpenses,
)


class CategoriesModelTest(TestCase):
    def test_returns_right_str(self):
        category = Categories.objects.create(name="test")
        self.assertEqual(str(category), "test")


class UsualExpensesModelTest(TestCase):
    def test_returns_right_str(self):
        category = Categories.objects.create(name="test")
        expense = UsualExpenses.objects.create(
            date=date(2022, 1, 1), category=category, amount=Decimal(1)
        )
        self.assertEqual(str(expense), 'Usual: 2022-01-01 category "test" value 1.00')

    def test_returns_in_right_order(self):
        category = Categories.objects.create(name="test")
        ex1 = UsualExpenses.objects.create(
            date=date(2022, 1, 1), category=category, amount=Decimal(1)
        )
        ex2 = UsualExpenses.objects.create(
            date=date(2022, 1, 2), category=category, amount=Decimal(2)
        )
        ex4 = UsualExpenses.objects.create(
            date=date(2022, 1, 4), category=category, amount=Decimal(4)
        )
        ex3 = UsualExpenses.objects.create(
            date=date(2022, 1, 3), category=category, amount=Decimal(3)
        )

        exp_list = list(UsualExpenses.objects.all())
        right_order = [ex4, ex3, ex2, ex1]
        self.assertEqual(exp_list, right_order)

    def test_get_objects_in_month(self):
        category = Categories.objects.create(name="test")
        UsualExpenses.objects.create(
            category=category, amount=Decimal(100), date=date(2022, 5, 5)
        )
        UsualExpenses.objects.create(
            category=category, amount=Decimal(500), date=date(2022, 5, 7)
        )
        UsualExpenses.objects.create(
            category=category, amount=Decimal(450), date=date(2022, 6, 5)
        )
        self.assertEqual(len(UsualExpenses.get_objects_in_month(2022, 5)), 2)
        self.assertEqual(len(UsualExpenses.get_objects_in_month(2022, 6)), 1)
        self.assertEqual(len(UsualExpenses.get_objects_in_month(2022, 7)), 0)

    def test_sum_of_some_incomes(self):
        category = Categories.objects.create(name="test")
        UsualExpenses.objects.create(
            category=category, amount=Decimal(100), date=date(2022, 5, 5)
        )
        UsualExpenses.objects.create(
            category=category, amount=Decimal(500), date=date(2022, 5, 7)
        )
        UsualExpenses.objects.create(
            category=category, amount=Decimal(450), date=date(2022, 6, 5)
        )
        self.assertEqual(UsualExpenses.get_sum_in_month(2022, 5), Decimal(600))
        self.assertEqual(UsualExpenses.get_sum_in_month(2022, 6), Decimal(450))
        self.assertEqual(UsualExpenses.get_sum_in_month(2022, 7), Decimal(0))


class ConstExpensesModelTest(TestCase):
    def setUp(self):
        ConstantExpenses.objects.create(
            name="phone", start_date=date(2021, 1, 1), value=Decimal(100)
        )

    def test_const_expense_creates_history_at_creation(self):
        expense = ConstantExpenses.objects.get(name="phone")
        history_object = ConstantExpenseHistoryItem.objects.filter(expense=expense)
        self.assertEqual(len(history_object), 1)

    def test_returns_current_value(self):
        expense = ConstantExpenses.objects.get(name="phone")
        expense.bump(value=Decimal(200), date=date(2022, 1, 1))

        value = expense.get_current_value()
        self.assertEqual(value, Decimal(200))

    def test_get_objects_in_month(self):
        expense = ConstantExpenses.objects.get(name="phone")
        expense.delete()
        ConstantExpenses.objects.create(
            name="2020-2022", start_date=date(2020, 1, 1), value=Decimal(100)
        )
        ConstantExpenses.objects.create(
            name="2021-2023", start_date=date(2021, 1, 1), value=Decimal(340)
        )
        ConstantExpenses.objects.create(
            name="2017-2019", start_date=date(2017, 1, 1), value=Decimal(270)
        )
        self.assertEqual(len(ConstantExpenses.get_objects_in_month(2021, 5)), 2)
        self.assertEqual(len(ConstantExpenses.get_objects_in_month(2022, 6)), 1)
        self.assertEqual(len(ConstantExpenses.get_objects_in_month(2023, 7)), 0)

    def test_sum_of_some_incomes(self):
        expense = ConstantExpenses.objects.get(name="phone")
        expense.delete()
        ConstantExpenses.objects.create(
            name="2020-2022", start_date=date(2020, 1, 1), value=Decimal(100)
        )
        ConstantExpenses.objects.create(
            name="2021-2023", start_date=date(2021, 1, 1), value=Decimal(340)
        )
        ConstantExpenses.objects.create(
            name="2017-2019", start_date=date(2017, 1, 1), value=Decimal(270)
        )
        self.assertEqual(ConstantExpenses.get_sum_in_month(2021, 5), Decimal(440))
        self.assertEqual(ConstantExpenses.get_sum_in_month(2022, 6), Decimal(340))
        self.assertEqual(ConstantExpenses.get_sum_in_month(2023, 7), Decimal(0))
