from datetime import date, datetime
from decimal import Decimal
from re import L
from django.test import TestCase
from django.contrib.auth import get_user_model

from expenses.forms import UsualExpenseAddForm, CategoryAddForm
from expenses.models import Categories

User = get_user_model()


class AddUsualExpensePageTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        self.client.logout()
        response = self.client.get(f"/expenses/add")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/expenses/add",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_expense_template(self):
        """тест: используется правильный шаблон"""
        response = self.client.get(f"/expenses/add")
        self.assertTemplateUsed(response, "add_usual_expense.html")

    def test_has_add_usual_expense_form(self):
        response = self.client.get(f"/expenses/add")
        self.assertIsInstance(response.context["expense_form"], UsualExpenseAddForm)

    def test_has_add_category_form(self):
        response = self.client.get(f"/expenses/add")
        self.assertIsInstance(response.context["category_form"], CategoryAddForm)

    def test_show_category_in_select(self):
        Categories.objects.create(name='apple')
        response = self.client.get(f"/expenses/add")
        self.assertContains(response, 'apple', 2)

