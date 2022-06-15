from datetime import date, datetime
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from goals.models import Goals, GoalStatus
from goals.forms import GoalBumpForm, GoalEditForm

User = get_user_model()


class AllGoalsPageTest(TestCase):
    """тесты для странички, где отображаются все цели"""

    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть список целей неавторизованным"""
        self.client.logout()
        response = self.client.get(f"/goals/")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/goals/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_uses_all_goals_template(self):
        """тест: используется правильный шаблон"""
        response = self.client.get(f"/goals/")
        self.assertTemplateUsed(response, "all_goals.html")

    def test_contains_goals(self):
        """тест: страничка содержит все созданные цели"""
        Goals.objects.create(name="car", date=date(2021, 12, 31), value=Decimal(10.0))
        Goals.objects.create(name="house", date=date(2023, 12, 31), value=Decimal(30.0))

        response = self.client.get(f"/goals/")

        self.assertContains(response, "car")
        self.assertContains(response, "house")

    def test_page_contain_data_from_goal(self):
        """тест: на страничке с целями отображается инфа сколько процентов осталось, сколько осталось, сколько всего"""
        goal = Goals.objects.create(
            name="car", date=date(2023, 12, 31), value=Decimal(10.0)
        )
        goal.bump(date=date(2022, 12, 31), value=Decimal(5.0))

        response = self.client.get(f"/goals/")

        self.assertContains(response, "Left <strong>5,00</strong> of 10,00")
        self.assertContains(response, "50,00 %")


class GoalPageTest(TestCase):
    """тест странички с целью"""

    def setUp(self) -> None:
        Goals.objects.create(name="car", date=date(2023, 12, 31), value=Decimal(10.0))
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        Goals.objects.get(name="car").delete()
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть цель неавторизованным"""
        goal = Goals.objects.get(name="car")
        self.client.logout()
        response = self.client.get(f"/goals/{goal.id}")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/goals/{goal.id}",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_history_is_shown(self):

        goal = Goals.objects.get(name="car")

        goal.bump(date=date(2022, 6, 30), value=Decimal(2.0))
        goal.bump(date=date(2022, 7, 31), value=Decimal(2.0))

        response = self.client.get(goal.get_absolute_url())

        self.assertContains(response, "31 июля 2022 г.")
        self.assertContains(response, "30 июня 2022 г.")


class GoalEditPageTest(TestCase):
    def setUp(self) -> None:
        Goals.objects.create(name="car", date=date(2023, 12, 31), value=Decimal(10.0))
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть цель неавторизованным"""
        goal = Goals.objects.get(name="car")
        self.client.logout()
        response = self.client.get(f"/goals/{goal.id}")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/goals/{goal.id}",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_passes_correct_list_to_template(self):
        """тест: вызывается правильный шаблон"""
        goal = Goals.objects.get(name="car")
        response = self.client.get(f"/goals/{goal.id}/edit")
        self.assertTemplateUsed(response, "edit_goal.html")

    def test_using_bump_goal_form(self):
        goal = Goals.objects.get(name="car")
        response = self.client.get(f"/goals/{goal.id}/edit")
        self.assertIsInstance(response.context["form"], GoalEditForm)

    def test_saves_post_request(self):
        goal = Goals.objects.get(name="car")
        self.client.post(
            f"/goals/{goal.id}/edit",
            data={"name": "car1", "date": date(2021, 1, 1), "value": "1000.00"},
        )
        new_date = Goals.objects.first().date
        self.assertEqual(new_date, date(2021, 1, 1))

    def test_POST_redirects_to_list_view(self):
        """тест: переадресуется в представление списка"""
        goal = Goals.objects.get(name="car")
        response = self.client.post(
            f"/goals/{goal.id}/bump",
            data={"date": f"{date(2021, 1, 1)}", "value": "100"},
        )
        self.assertRedirects(response, "/goals/")


class GoalBumpPageTest(TestCase):
    def setUp(self) -> None:
        Goals.objects.create(name="car", date=date(2023, 12, 31), value=Decimal(10.0))
        user = User.objects.create(username="tester")
        self.client.force_login(user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_access_denied_to_unauthenticated_user(self):
        """тест: нельзя посмотреть цель неавторизованным"""
        goal = Goals.objects.get(name="car")
        self.client.logout()
        response = self.client.get(f"/goals/{goal.id}")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/goals/{goal.id}",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_passes_correct_list_to_template(self):
        """тест: вызывается правильный шаблон"""
        goal = Goals.objects.get(name="car")
        response = self.client.get(f"/goals/{goal.id}/bump")
        self.assertTemplateUsed(response, "bump_goal.html")

    def test_using_bump_goal_form(self):
        goal = Goals.objects.get(name="car")
        response = self.client.get(f"/goals/{goal.id}/bump")
        self.assertIsInstance(response.context["form"], GoalBumpForm)

    def test_saves_post_request(self):
        goal = Goals.objects.get(name="car")
        self.client.post(
            f"/goals/{goal.id}/bump",
            data={"date": f"{date(2021, 1, 1)}", "value": "100"},
        )
        self.assertEqual(GoalStatus.objects.count(), 2)

    def test_POST_redirects_to_current_goal(self):
        """тест: переадресуется в конкретную цель"""
        goal = Goals.objects.get(name="car")
        response = self.client.post(
            f"/goals/{goal.id}/edit",
            data={"name": "test1", "date": date(2021, 1, 1), "value": "100"},
        )
        self.assertRedirects(response,
            goal.get_absolute_url(),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,)
