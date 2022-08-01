from datetime import date, datetime
from decimal import Decimal
from django.test import TestCase

from monthly.models import FreeMoney


class FreeMoneyModelTest(TestCase):
    def setUp(self):
        FreeMoney.objects.create(date=date(2021, 1, 1), value=Decimal(100))

    def test_returns_get_value(self):
        FreeMoney.bump(value=Decimal(200), date=date(2022, 3, 1))

        value1 = FreeMoney.get_value(2021, 1)
        value2 = FreeMoney.get_value(2022, 3)
        value3 = FreeMoney.get_value(2020, 1)
        self.assertEqual(value1, Decimal(100))
        self.assertEqual(value2, Decimal(200))
        self.assertEqual(value3, Decimal(0))
