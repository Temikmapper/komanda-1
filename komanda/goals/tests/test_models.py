from datetime import date
from decimal import Decimal
from unittest import skip
from django.test import TestCase

from goals.models import Goals, GoalExpense, GoalBump


class GoalsModelTest(TestCase):
    """Тестирование моделей для целей"""

    def setUp(self):
        global goal
        Goals.objects.create(name="car", date=date(2023, 12, 31), value=Decimal(10.0))

    def tearDown(self):
        goal = Goals.objects.get(name="car")
        goal.delete()

    def test_goal_prints_its_name(self):
        goal = Goals.objects.get(name="car")
        self.assertEqual(goal.name, str(goal))

    @skip
    def test_goal_creates_history_at_creation(self):
        goal = Goals.objects.get(name="car")
        history_object = GoalExpense.objects.filter(goal=goal)
        self.assertEqual(len(history_object), 1)

    @skip
    def test_goal_get_left(self):
        """тест: получение сколько осталось накопить"""
        goal = Goals.objects.get(name="car")
        goal.add_expense(Decimal(5.0), date=date(2022, 1, 1))
        goal.add_expense(Decimal(1.0), date=date(2022, 1, 1))
        self.assertEqual(goal.get_left(), Decimal(4.0))

    @skip
    def test_goal_returns_percent(self):
        """тест: цель возвращает сколько накоплено в процентах"""
        goal = Goals.objects.all()[0]
        goal.add_expense(Decimal(5.0), date=date(2022, 1, 1))
        percent = goal.get_percent()
        self.assertEqual(percent, Decimal(50.0))

    def test_goal_returns_accumulated(self):
        goal = Goals.objects.create(
            name="house", date=date(2023, 12, 31), value=Decimal(100.0)
        )

        GoalExpense.objects.create(
            goal=goal, value=Decimal(10.0), date=date(2023, 1, 31)
        )
        GoalExpense.objects.create(
            goal=goal, value=Decimal(30.0), date=date(2023, 2, 15)
        )
        GoalExpense.objects.create(
            goal=goal, value=Decimal(10.0), date=date(2023, 3, 15)
        )

        spent_by_june = goal.get_spent_by_month(year=2023, month=6)
        self.assertEqual(spent_by_june, Decimal(50.0))
        spent_by_february = goal.get_spent_by_month(year=2023, month=2)
        self.assertEqual(spent_by_february, Decimal(40))
        spent_by_2022 = goal.get_spent_by_month(year=2022, month=12)
        self.assertEqual(spent_by_2022, Decimal(0))

        goal.add_expense(Decimal(3.0), date=date(2022, 1, 1))
        goal.add_expense(Decimal(4.0), date=date(2022, 1, 2))
        accumulated = goal.get_accumulated()
        self.assertEqual(accumulated, Decimal(7.0))

    @skip
    def test_goal_return_beautiful_string(self):
        """тест: при обращении к методам цели, они возвращают десятичные с двумя знаками после запятой"""
        goal = Goals.objects.all()[0]
        goal.add_expense(Decimal(5.0), date=date(2022, 1, 1))
        percent = str(goal.get_percent())
        left = str(goal.get_left())
        accumulated = str(goal.get_accumulated())
        self.assertEqual(accumulated, "5.00")
        self.assertEqual(percent, "50.00")
        self.assertEqual(left, "5.00")

    def test_goal_returns_its_expenses_history_in_right_order(self):
        """тест: цель возвращает свою историю в правильном порядке"""
        goal = Goals.objects.all()[0]
        bump1 = goal.add_expense(Decimal(1.0), date=date(2023, 1, 1))
        bump2 = goal.add_expense(Decimal(2.0), date=date(2023, 1, 1))
        bump4 = goal.add_expense(Decimal(5.0), date=date(2023, 1, 5))
        bump3 = goal.add_expense(Decimal(1.0), date=date(2023, 1, 2))

        goal_history_list = goal.get_expenses_list()
        right_order = [bump1, bump2, bump3, bump4]
        self.assertEqual(goal_history_list, right_order)

    def test_goal_add_bumps(self):
        goal = Goals.objects.create(
            name="car", date=date(2023, 12, 31), value=Decimal(10.0)
        )
        GoalBump.objects.create(goal=goal, value=Decimal(10.0), date=date(2023, 1, 31))
        GoalBump.objects.create(goal=goal, value=Decimal(30.0), date=date(2023, 2, 15))
        GoalBump.objects.create(goal=goal, value=Decimal(10.0), date=date(2023, 3, 15))

        accumulated_by_june = goal.get_accumulated_by_month(year=2023, month=6)
        self.assertEqual(accumulated_by_june, Decimal(50.0))
        accumulated_by_february = goal.get_accumulated_by_month(year=2023, month=2)
        self.assertEqual(accumulated_by_february, Decimal(40))
        accumulated_by_2022 = goal.get_accumulated_by_month(year=2022, month=12)
        self.assertEqual(accumulated_by_2022, Decimal(0))

        goal.delete()

    def test_goal_balance(self):
        goal = Goals.objects.create(
            name="boat", date=date(2023, 12, 31), value=Decimal(1000.0)
        )
        GoalBump.objects.create(goal=goal, value=Decimal(100.0), date=date(2023, 1, 30))
        GoalExpense.objects.create(
            goal=goal, value=Decimal(10.0), date=date(2023, 1, 31)
        )

        GoalBump.objects.create(goal=goal, value=Decimal(30.0), date=date(2023, 2, 15))
        GoalExpense.objects.create(
            goal=goal, value=Decimal(40.0), date=date(2023, 2, 16)
        )

        GoalBump.objects.create(goal=goal, value=Decimal(50.0), date=date(2023, 3, 15))
        GoalExpense.objects.create(
            goal=goal, value=Decimal(10.0), date=date(2023, 3, 17)
        )

        balance_by_june = goal.get_balance_by_month(year=2023, month=6)
        self.assertEqual(balance_by_june, Decimal(120.0))
        balance_by_february = goal.get_balance_by_month(year=2023, month=2)
        self.assertEqual(balance_by_february, Decimal(80))
        balance_by_2022 = goal.get_balance_by_month(year=2022, month=12)
        self.assertEqual(balance_by_2022, Decimal(0))

    def test_get_expenses_value_in_month(self):
        goal = Goals.objects.create(
            name="rocket", date=date(2023, 12, 31), value=Decimal(10000.0)
        )

        GoalExpense.objects.create(
            goal=goal, value=Decimal(10.0), date=date(2023, 1, 31)
        )
        GoalExpense.objects.create(
            goal=goal, value=Decimal(30.0), date=date(2023, 1, 15)
        )
        GoalExpense.objects.create(
            goal=goal, value=Decimal(200.0), date=date(2023, 1, 15)
        )

        result_at_jan = goal.get_expenses_value_in_month(2023, 1)
        result_at_feb = goal.get_expenses_value_in_month(2023, 2)

        self.assertEqual(result_at_jan, Decimal(240))
        self.assertEqual(result_at_feb, 0)