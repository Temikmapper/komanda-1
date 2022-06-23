from datetime import date
from decimal import Decimal
from unittest import skip
from django.test import TestCase
from django.contrib.auth import get_user_model

from expenses.models import ConstantExpenses, Categories, UsualExpenses
from incomes.models import ConstantIncomes

User = get_user_model()


class MonthlyPageWithoutArgumentsTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: не откроется неавторизованному пользователю"""
        self.client.logout()
        response = self.client.get("/monthly/")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/monthly/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class MonthlyPageTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: не откроется неавторизованному пользователю"""
        self.client.logout()
        response = self.client.get(f"/monthly/{date.today().year}/{date.today().month}")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/monthly/{date.today().year}/{date.today().month}",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_monthly_template(self):
        """тест: используется правильный шаблон"""
        response = self.client.get(f"/monthly/{date.today().year}/{date.today().month}")
        self.assertTemplateUsed(response, "monthly.html")

    def test_contains_const_expenses(self):
        ConstantExpenses.objects.create(
            start_date=date(2020, 1, 1), name="test", value=Decimal(100)
        )
        ConstantExpenses.objects.create(
            start_date=date(2020, 2, 1), name="test", value=Decimal(200)
        )
        response = self.client.get("/monthly/2020/3")
        self.assertContains(response, "300,00")
        response = self.client.get("/monthly/2020/1")
        self.assertContains(response, "100,00")
        response = self.client.get("/monthly/2019/12")
        self.assertContains(response, "0,00")

    def test_contains_const_incomes(self):
        ConstantIncomes.objects.create(
            start_date=date(2020, 3, 1), name="test", value=Decimal(150)
        )
        ConstantIncomes.objects.create(
            start_date=date(2020, 4, 1), name="test", value=Decimal(220)
        )
        response = self.client.get("/monthly/2020/5")
        self.assertContains(response, "370,00")
        response = self.client.get("/monthly/2020/3")
        self.assertContains(response, "150,00")
        response = self.client.get("/monthly/2020/2")
        self.assertContains(response, "0,00")

    def test_contains_free_money(self):
        pass  # TODO free money

    def test_contains_usual_expenses(self):
        category1 = Categories.objects.create(name="apple")
        category2 = Categories.objects.create(name="ananas")
        UsualExpenses.objects.create(
            category=category1, amount=Decimal(20), date=date(2020, 1, 2)
        )
        UsualExpenses.objects.create(
            category=category2, amount=Decimal(40), date=date(2020, 1, 5)
        )
        response = self.client.get("/monthly/2020/1")
        self.assertContains(response, "apple")
        self.assertContains(response, "ananas")
        self.assertContains(response, "60")
        self.assertContains(response, "20")
        self.assertContains(response, "40")
        response = self.client.get("/monthly/2020/2")
        self.assertNotContains(response, "apple")
        self.assertNotContains(response, "ananas")
