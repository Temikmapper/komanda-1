from datetime import date, datetime
from decimal import Decimal
from django.test import TestCase

from expenses.models import Categories, UsualExpenses


class CategoriesModelTest(TestCase):
    
    def test_returns_right_str(self):
        category = Categories.objects.create(name="test")
        self.assertEqual(str(category), "test")

class ExpensesModelTest(TestCase):

    def test_returns_right_str(self):
        category = Categories.objects.create(name="test")
        expense = UsualExpenses.objects.create(date=date(2022,1,1), category=category, amount=Decimal(1))
        self.assertEqual(str(expense), "Usual: 2022-01-01 category \"test\" value 1.00")

    def test_returns_in_right_order(self):
        category = Categories.objects.create(name="test")
        ex1 = UsualExpenses.objects.create(date=date(2022,1,1), category=category, amount=Decimal(1))
        ex2 = UsualExpenses.objects.create(date=date(2022,1,2), category=category, amount=Decimal(2))
        ex4 = UsualExpenses.objects.create(date=date(2022,1,4), category=category, amount=Decimal(4))
        ex3 = UsualExpenses.objects.create(date=date(2022,1,3), category=category, amount=Decimal(3))

        exp_list = list(UsualExpenses.objects.all())
        right_order = [ex4, ex3, ex2, ex1]
        self.assertEqual(exp_list, right_order)
