from datetime import date
from decimal import Decimal
from unittest import skip
from django.test import TestCase
from django.contrib.auth import get_user_model

from expenses.models import ConstantExpenses, Categories, UsualExpenses
from incomes.models import ConstantIncomes
from monthly.forms import BumpFreeMoneyForm
from monthly.models import FreeMoney

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
        response = self.client.get("/monthly/2020/5")
        self.assertContains(response, "Free: <span id=\"free_money\">0,00")
        FreeMoney.bump(date=date(2020, 5, 1), value=Decimal(100))
        response = self.client.get("/monthly/2020/5")
        self.assertContains(response, "Free: <span id=\"free_money\">100,00")
        response = self.client.get("/monthly/2020/4")
        self.assertContains(response, "Free: <span id=\"free_money\">0,00")


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

class BumpFreeMoneyPageTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        self.client.logout()
        response = self.client.get(f"/monthly/{date.today().year}/{date.today().month}/bump_free_money")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/monthly/{date.today().year}/{date.today().month}/bump_free_money",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_template(self):
        """тест: используется правильный шаблон"""
        response = self.client.get(f"/monthly/{date.today().year}/{date.today().month}/bump_free_money")
        self.assertTemplateUsed(response, "bump_free_money.html")

    def test_has_form(self):
        response = self.client.get(f"/monthly/{date.today().year}/{date.today().month}/bump_free_money")
        self.assertIsInstance(response.context["form"], BumpFreeMoneyForm)

    def test_saves_post_request(self):
        response = self.client.post(
            f"/monthly/2021/01/bump_free_money",
            data={"date": "2021-01-01", "value": "100"},
        )
        self.assertEqual(FreeMoney.objects.count(), 1)

    def test_redirects_to_monthly_page_after_saving(self):
        response = self.client.post(
            f"/monthly/2021/01/bump_free_money",
            data={"date": "2021-01-01", "value": "100"},
        )
        self.assertRedirects(
            response,
            "/monthly/",
            status_code=302,
            target_status_code=302,
            fetch_redirect_response=True,
        )