from datetime import date
from decimal import Decimal
from unittest import skip
from django.test import TestCase
from django.contrib.auth import get_user_model

from expenses.forms import (
    UsualExpenseAddForm,
    CategoryAddForm,
    ConstExpenseAddForm,
    ConstExpenseHistoryAddForm,
)
from expenses.models import (
    Categories,
    ConstantExpenseHistoryItem,
    ConstantExpenses,
    UsualExpenses,
)
from expenses.forms import ConstExpenseEditForm, BumpExpenseForm

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
        response = self.client.get("/expenses/add")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/expenses/add",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_expense_template(self):
        """тест: используется правильный шаблон"""
        response = self.client.get("/expenses/add")
        self.assertTemplateUsed(response, "add_usual_expense.html")

    def test_has_add_usual_expense_form(self):
        response = self.client.get("/expenses/add")
        self.assertIsInstance(response.context["expense_form"], UsualExpenseAddForm)

    def test_has_add_category_form(self):
        response = self.client.get("/expenses/add")
        self.assertIsInstance(response.context["category_form"], CategoryAddForm)

    def test_show_category_in_select(self):
        Categories.objects.create(name="apple")
        response = self.client.get("/expenses/add")
        self.assertContains(response, "apple", 3)

    def test_saves_post_request(self):
        Categories.objects.create(name="apple")
        category = Categories.objects.get(name="apple")
        response = self.client.post(
            "/expenses/add",
            data={"category": f"{category.id}", "date": "2021-01-01", "amount": "10"},
        )
        self.assertEqual(UsualExpenses.objects.count(), 1)


class AddConstExpensePageTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        self.client.logout()
        response = self.client.get("/expenses/add_constant")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/expenses/add_constant",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_expense_template(self):
        """тест: используется правильный шаблон"""
        response = self.client.get("/expenses/add_constant")
        self.assertTemplateUsed(response, "add_const_expense.html")

    def test_has_add_usual_expense_form(self):
        response = self.client.get("/expenses/add_constant")
        self.assertIsInstance(response.context["expense_form"], ConstExpenseAddForm)
        self.assertIsInstance(
            response.context["expense_value_form"], ConstExpenseHistoryAddForm
        )

    def test_saves_post_request(self):
        response = self.client.post(
            "/expenses/add_constant",
            data={"name": "test1", "start_date": "2021-01-01", "value": "100"},
        )
        self.assertEqual(ConstantExpenses.objects.count(), 1)
        self.assertEqual(ConstantExpenseHistoryItem.objects.count(), 1)

    def test_redirects_to_all_page_after_saving(self):
        response = self.client.post(
            "/expenses/add_constant",
            data={"name": "test1", "start_date": "2021-01-01", "value": "100"},
        )
        self.assertRedirects(
            response,
            "/expenses/constant/all",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class ViewAllConstExpensesTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        self.client.logout()
        response = self.client.get("/expenses/constant/all")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/expenses/constant/all",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_expense_template(self):
        """тест: используется правильный шаблон"""
        response = self.client.get("/expenses/constant/all")
        self.assertTemplateUsed(response, "view_all_constant_expenses.html")

    def test_shows_outdated_expenses(self):
        ConstantExpenses.objects.create(
            name="oldman", start_date=date(2010, 1, 1), value=Decimal(100)
        )
        response = self.client.get("/expenses/constant/all")
        self.assertContains(response, "outdated_expense_item")


class ViewConstExpenseTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        ConstantExpenses.objects.create(
            name="phone", start_date=date(2021, 1, 1), value=Decimal(100)
        )
        self.client.force_login(user)

    def tearDown(self) -> None:
        ConstantExpenses.objects.get(name="phone").delete()
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        expense = ConstantExpenses.objects.get(name="phone")
        self.client.logout()
        response = self.client.get(expense.get_absolute_url())
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/expenses/constant/{expense.id}",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_expense_template(self):
        """тест: используется правильный шаблон"""
        expense = ConstantExpenses.objects.get(name="phone")
        response = self.client.get(expense.get_absolute_url())
        self.assertTemplateUsed(response, "view_constant_expense.html")

    def test_history_is_shown(self):

        expense = ConstantExpenses.objects.get(name="phone")

        expense.bump(date=date(2022, 6, 30), value=Decimal(2.0))
        expense.bump(date=date(2022, 7, 31), value=Decimal(3.0))

        response = self.client.get(expense.get_absolute_url())

        self.assertContains(response, "31 июля 2022 г.")
        self.assertContains(response, "30 июня 2022 г.")


class EditConstExpenseTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        ConstantExpenses.objects.create(
            name="phone", start_date=date(2021, 1, 1), value=Decimal(100)
        )
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        expense = ConstantExpenses.objects.get(name="phone")
        self.client.logout()
        response = self.client.get(expense.get_absolute_url() + "/edit")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/expenses/constant/{expense.id}/edit",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_expense_template(self):
        """тест: используется правильный шаблон"""
        expense = ConstantExpenses.objects.get(name="phone")
        response = self.client.get(expense.get_absolute_url() + "/edit")
        self.assertTemplateUsed(response, "edit_constant_expense.html")

    def test_using_edit_expense_form(self):
        expense = ConstantExpenses.objects.get(name="phone")
        response = self.client.get(expense.get_absolute_url() + "/edit")
        self.assertIsInstance(response.context["form"], ConstExpenseEditForm)

    def test_saves_post_request(self):
        expense = ConstantExpenses.objects.get(name="phone")
        self.client.post(
            expense.get_absolute_url() + "/edit",
            data={
                "name": "phone1",
                "start_date": date(2022, 1, 1),
                "finish_date": date(2023, 1, 1),
            },
        )
        new_start_date = ConstantExpenses.objects.first().start_date
        new_finish_date = ConstantExpenses.objects.first().finish_date
        self.assertEqual(new_start_date, date(2022, 1, 1))
        self.assertEqual(new_finish_date, date(2023, 1, 1))

    def test_POST_redirects_to_list_view(self):
        """тест: переадресуется в представление списка"""
        expense = ConstantExpenses.objects.get(name="phone")
        response = self.client.post(
            expense.get_absolute_url() + "/edit",
            data={
                "name": "phone1",
                "start_date": date(2022, 1, 1),
                "finish_date": date(2023, 1, 1),
            },
        )
        self.assertRedirects(response, "/expenses/constant/all")


class BumpConstExpenseTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        ConstantExpenses.objects.create(
            name="phone", start_date=date(2021, 1, 1), value=Decimal(100)
        )
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        expense = ConstantExpenses.objects.get(name="phone")
        self.client.logout()
        response = self.client.get(expense.get_absolute_url() + "/bump")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/expenses/constant/{expense.id}/bump",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_expense_template(self):
        """тест: используется правильный шаблон"""
        expense = ConstantExpenses.objects.get(name="phone")
        response = self.client.get(expense.get_absolute_url() + "/bump")
        self.assertTemplateUsed(response, "bump_constant_expense.html")

    def test_using_edit_expense_form(self):
        expense = ConstantExpenses.objects.get(name="phone")
        response = self.client.get(expense.get_absolute_url() + "/bump")
        self.assertIsInstance(response.context["form"], BumpExpenseForm)

    def test_saves_post_request(self):
        expense = ConstantExpenses.objects.get(name="phone")
        self.client.post(
            expense.get_absolute_url() + "/bump",
            data={"date": date(2022, 1, 1), "value": "1000"},
        )
        new_value = ConstantExpenses.objects.first().get_current_value()
        self.assertEqual(new_value, Decimal(1000))

    def test_POST_redirects_to_list_view(self):
        """тест: переадресуется в представление списка"""
        expense = ConstantExpenses.objects.get(name="phone")
        response = self.client.post(
            expense.get_absolute_url() + "/bump",
            data={"date": date(2022, 1, 1), "value": "1000"},
        )
        self.assertRedirects(response, "/expenses/constant/all")

    def test_redirects_to_all_if_outdated_expense(self):
        ConstantExpenses.objects.create(
            name="old", start_date=date(2010, 1, 1), value=Decimal(10.0)
        )
        expense = ConstantExpenses.objects.get(name="old")
        response = self.client.post(
            expense.get_absolute_url() + "/bump",
            data={"date": date(2022, 1, 1), "value": "1000"},
        )
        items = ConstantExpenseHistoryItem.objects.filter(expense=expense)
        self.assertEqual(len(items), 1)
        self.assertRedirects(response, "/expenses/constant/all")

    def test_delete_constant_expense(self):
        expense = ConstantExpenses.objects.get(name="phone")
        response = self.client.get(expense.get_absolute_url() + "/delete")
        self.assertEqual(ConstantExpenses.objects.count(), 0)
        self.assertRedirects(response, "/expenses/constant/all")
