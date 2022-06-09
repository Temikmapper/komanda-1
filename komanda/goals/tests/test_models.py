from datetime import date, datetime
from decimal import Decimal
from django.test import TestCase

from goals.models import Goals, GoalStatus


class GoalsModelTest(TestCase):
    """Тестирование моделей для целей"""

    def test_goal_prints_its_name(self):
        goal = Goals.objects.create(name="car", date=datetime.today(), value=Decimal(10.0))
        self.assertEqual(goal.name, str(goal))

    def test_goal_creates_history_at_creation(self):
        goal = Goals.objects.create(name="car", date=datetime.today(), value=Decimal(10.0))
        history_object = GoalStatus.objects.filter(goal=goal)
        self.assertEqual(len(history_object), 1)

    def test_creates_status_after_bump(self):
        """тест: пополнение цели
        """
        goal = Goals.objects.create(name="car", date=datetime.today(), value=Decimal(10.0))
        goal.bump(Decimal(1.0), date=date(2022,1,1))
        last_status = GoalStatus.objects.last()
        self.assertEqual(last_status.value, Decimal(1.0))

    def test_goal_get_current_value(self):
        goal = Goals.objects.create(name="car", date=datetime.today(), value=Decimal(10.0))
        goal.bump(Decimal(5.0))
        self.assertEqual(goal.left, Decimal(5.0))
