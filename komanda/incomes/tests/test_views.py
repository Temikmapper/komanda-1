from datetime import date
from decimal import Decimal
from unittest import skip
from django.test import TestCase
from django.contrib.auth import get_user_model

from incomes.forms import (
    ConstIncomeAddForm,
    ConstantIncomeEditForm,
    BumpIncomeForm,
)
from incomes.models import ConstantIncomeHistoryItem, ConstantIncomes

User = get_user_model()


class AddConstIncomePageTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        self.client.logout()
        response = self.client.get("/incomes/add_constant")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/incomes/add_constant",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_income_template(self):
        """тест: используется правильный шаблон"""
        response = self.client.get("/incomes/add_constant")
        self.assertTemplateUsed(response, "add_const_income.html")

    def test_has_add_usual_income_form(self):
        response = self.client.get("/incomes/add_constant")
        self.assertIsInstance(response.context["income_form"], ConstIncomeAddForm)
        self.assertIsInstance(
            response.context["income_value_form"], ConstIncomeHistoryAddForm
        )

    def test_saves_post_request(self):
        self.client.post(
            "/incomes/add_constant",
            data={"name": "test1", "start_date": "2021-01-01", "value": "100"},
        )
        self.assertEqual(ConstantIncomes.objects.count(), 1)
        self.assertEqual(ConstantIncomeHistoryItem.objects.count(), 1)

    def test_redirects_to_all_page_after_saving(self):
        response = self.client.post(
            "/incomes/add_constant",
            data={"name": "test1", "start_date": "2021-01-01", "value": "100"},
        )
        self.assertRedirects(
            response,
            "/incomes/constant/all",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class ViewAllConstIncomesTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        self.client.logout()
        response = self.client.get("/incomes/constant/all")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/incomes/constant/all",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_income_template(self):
        """тест: используется правильный шаблон"""
        response = self.client.get("/incomes/constant/all")
        self.assertTemplateUsed(response, "view_all_constant_incomes.html")

    @skip
    def test_shows_outdated_incomes(self):
        ConstantIncomes.objects.create(
            name="oldman", start_date=date(2010, 1, 1), value=Decimal(100)
        )
        response = self.client.get("/incomes/constant/all")
        self.assertContains(response, "outdated_income_item")

    @skip
    def test_show_income_in_month(self):
        ConstantIncomes.objects.create(
            name="NovemberSalary", start_date=date(2022, 10, 15), value=Decimal(30000)
        )
        response = self.client.get("/incomes/constant/all")
        self.assertContains(response, "30 000")



class ViewConstIncomeTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        ConstantIncomes.objects.create(
            name="phone", start_date=date(2021, 1, 1), value=Decimal(100)
        )
        self.client.force_login(user)

    def tearDown(self) -> None:
        ConstantIncomes.objects.get(name="phone").delete()
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        income = ConstantIncomes.objects.get(name="phone")
        self.client.logout()
        response = self.client.get(income.get_absolute_url())
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/incomes/constant/{income.id}",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_income_template(self):
        """тест: используется правильный шаблон"""
        income = ConstantIncomes.objects.get(name="phone")
        response = self.client.get(income.get_absolute_url())
        self.assertTemplateUsed(response, "view_constant_income.html")

    def test_history_is_shown(self):

        income = ConstantIncomes.objects.get(name="phone")

        income.bump(date=date(2022, 6, 30), value=Decimal(2.0))
        income.bump(date=date(2022, 7, 31), value=Decimal(3.0))

        response = self.client.get(income.get_absolute_url())

        self.assertContains(response, "31 июля 2022 г.")
        self.assertContains(response, "30 июня 2022 г.")


class EditConstIncomeTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        ConstantIncomes.objects.create(
            name="phone", start_date=date(2021, 1, 1), value=Decimal(100)
        )
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        income = ConstantIncomes.objects.get(name="phone")
        self.client.logout()
        response = self.client.get(income.get_absolute_url() + "/edit")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/incomes/constant/{income.id}/edit",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_income_template(self):
        """тест: используется правильный шаблон"""
        income = ConstantIncomes.objects.get(name="phone")
        response = self.client.get(income.get_absolute_url() + "/edit")
        self.assertTemplateUsed(response, "edit_constant_income.html")

    def test_using_edit_income_form(self):
        income = ConstantIncomes.objects.get(name="phone")
        response = self.client.get(income.get_absolute_url() + "/edit")
        self.assertIsInstance(response.context["form"], ConstantIncomeEditForm)

    def test_saves_post_request(self):
        income = ConstantIncomes.objects.get(name="phone")
        self.client.post(
            income.get_absolute_url() + "/edit",
            data={
                "name": "phone1",
                "start_date": date(2022, 1, 1),
                "finish_date": date(2023, 1, 1),
            },
        )
        new_start_date = ConstantIncomes.objects.first().start_date
        new_finish_date = ConstantIncomes.objects.first().finish_date
        self.assertEqual(new_start_date, date(2022, 1, 1))
        self.assertEqual(new_finish_date, date(2023, 1, 1))

    def test_POST_redirects_to_list_view(self):
        """тест: переадресуется в представление списка"""
        income = ConstantIncomes.objects.get(name="phone")
        response = self.client.post(
            income.get_absolute_url() + "/edit",
            data={
                "name": "phone1",
                "start_date": date(2022, 1, 1),
                "finish_date": date(2023, 1, 1),
            },
        )
        self.assertRedirects(response, "/incomes/constant/all")


class BumpConstIncomeTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        ConstantIncomes.objects.create(
            name="phone", start_date=date(2021, 1, 1), value=Decimal(100)
        )
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        income = ConstantIncomes.objects.get(name="phone")
        self.client.logout()
        response = self.client.get(income.get_absolute_url() + "/bump")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/incomes/constant/{income.id}/bump",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_add_usual_income_template(self):
        """тест: используется правильный шаблон"""
        income = ConstantIncomes.objects.get(name="phone")
        response = self.client.get(income.get_absolute_url() + "/bump")
        self.assertTemplateUsed(response, "bump_constant_income.html")

    def test_using_edit_income_form(self):
        income = ConstantIncomes.objects.get(name="phone")
        response = self.client.get(income.get_absolute_url() + "/bump")
        self.assertIsInstance(response.context["form"], BumpIncomeForm)

    def test_saves_post_request(self):
        income = ConstantIncomes.objects.get(name="phone")
        self.client.post(
            income.get_absolute_url() + "/bump",
            data={"date": date(2022, 1, 1), "value": "1000"},
        )
        new_value = ConstantIncomes.objects.first().get_current_value()
        self.assertEqual(new_value, Decimal(1000))

    def test_POST_redirects_to_list_view(self):
        """тест: переадресуется в представление списка"""
        income = ConstantIncomes.objects.get(name="phone")
        response = self.client.post(
            income.get_absolute_url() + "/bump",
            data={"date": date(2022, 1, 1), "value": "1000"},
        )
        self.assertRedirects(response, "/incomes/constant/all")

    def test_redirects_to_all_if_outdated_income(self):
        ConstantIncomes.objects.create(
            name="old", start_date=date(2010, 1, 1), value=Decimal(10.0)
        )
        income = ConstantIncomes.objects.get(name="old")
        response = self.client.post(
            income.get_absolute_url() + "/bump",
            data={"date": date(2022, 1, 1), "value": "1000"},
        )
        items = ConstantIncomeHistoryItem.objects.filter(income=income)
        self.assertEqual(len(items), 1)
        self.assertRedirects(response, "/incomes/constant/all")

    def test_delete_constant_income(self):
        income = ConstantIncomes.objects.get(name="phone")
        response = self.client.get(income.get_absolute_url() + "/delete")
        self.assertEqual(ConstantIncomes.objects.count(), 0)
        self.assertRedirects(response, "/incomes/constant/all")
