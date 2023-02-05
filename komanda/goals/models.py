from calendar import monthrange
from datetime import date, datetime
from django.db.models import Sum
from decimal import ROUND_FLOOR, Decimal
from django.db import models
from django.utils import timezone


class Goals(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    value = models.DecimalField(max_digits=13, decimal_places=2)
    accumulated = models.DecimalField(
        max_digits=13, decimal_places=2, default=Decimal(0)
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/goals/{self.id}"

    def get_bump_url(self):
        return f"/goals/{self.id}/bump"

    def get_expense_url(self):
        return f"/goals/{self.id}/expense"

    def get_edit_url(self):
        return f"/goals/{self.id}/edit"

    def get_delete_url(self):
        return f"/goals/{self.id}/delete"

    def get_history(self):
        # TODO: объединить с Траты и бампы, сделать разделение на шаблоне
        return GoalExpense.objects.filter(goal=self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def add_expense(self, value, date):
        return GoalExpense.objects.create(date=date, value=value, goal=self)

    def bump(self, value, date):
        return GoalBump.objects.create(date=date, value=value, goal=self)

    def get_percent(self) -> Decimal:
        """Получить процент на сегодня

        Returns:
            Decimal: Баланс
        """
        balance = self.get_current_balance()
        if balance < 0:
            percent = Decimal(0)
        else:
            percent = (balance / self.value) * 100

        return percent.quantize(Decimal("1.00"), ROUND_FLOOR)

    def get_accumulated(self):
        return self.accumulated.quantize(Decimal("1.00"), ROUND_FLOOR)

    def get_expenses_list(self):
        statuses = GoalExpense.objects.filter(goal=self)
        return list(statuses)

    def get_current_balance(self) -> Decimal:
        """Получить баланс на сегодня

        Returns:
            Decimal: Баланс
        """
        today = date.today()
        return self.get_balance_by_month(year=today.year, month=today.month)

    def get_objects_in_month(
        self, object_type: models.Model, year: int, month: int
    ) -> models.QuerySet:
        """Получить объекты внутри месяца

        Args:
            object_type (models.Model): Тип объекта -- бампы или траты
            year (int): Год
            month (int): Месяц

        Returns:
            models.QuerySet: Queryset объектов
        """
        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)

        history_items = object_type.objects.filter(goal=self)
        objects_in_month = history_items.filter(
            date__lte=last_date_in_month, date__gte=first_date_in_month
        )

        return objects_in_month

    def get_expenses_in_month(self, year: int, month: int) -> models.QuerySet:
        """Получить список трат в месяце

        Args:
            year (int): Год
            month (Месяц): Месяц

        Returns:
            models.QuerySet: Queryset объектов
        """
        return self.get_objects_in_month(
            object_type=GoalExpense, year=year, month=month
        )

    def get_expenses_value_in_month(self, year: int, month: int) -> Decimal:
        """Получить сумму трат в месяце

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            Decimal: Сумма трат
        """

        result = self.get_expenses_in_month(year=year, month=month)
        if result:
            result = result.aggregate(Sum("value"))
            return result["value__sum"]
        else:
            return 0

    def get_bumps_in_month(self, year: int, month: int) -> models.QuerySet:
        """Получить queryset бампов в месяце

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            models.QuerySet: Queryset объектов
        """
        return self.get_objects_in_month(object_type=GoalBump, year=year, month=month)

    def get_bumps_value_in_month(self, year: int, month: int) -> Decimal:
        """Получить сумму поступлений в месяце

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            Decimal: Сумма поступлений
        """
        result = self.get_bumps_in_month(year=year, month=month)
        if result:
            result = result.aggregate(Sum("value"))
            return result["value__sum"]
        else:
            return 0

    def get_balance_by_month(self, year: int, month: int) -> Decimal:
        """Почитать баланс на месяц

        Args:
            year (int): Год, к которому нужно псчитать
            month (int): Месяц, к которому нужно посчитать

        Returns:
            Decimal: Посчитанный баланс
        """
        accumulated = self.get_accumulated_by_month(year=year, month=month)
        spent = self.get_spent_by_month(year=year, month=month)

        balance = accumulated - spent

        return balance

    def get_accumulated_by_month(self, year: int, month: int) -> Decimal:
        """Посчитать, сколько накоплено к году и месяцу

        Args:
            year (int): Год, к которому надо посчитать
            month (int): Месяц к которому надо посичтать

        Returns:
            Decimal: Посчитанная сумма
        """
        last_day = monthrange(year, month)[1]
        result = GoalBump.objects.filter(
            goal=self, date__lte=date(year=year, month=month, day=last_day)
        ).aggregate(Sum("value"))

        if not result["value__sum"]:
            return Decimal(0)
        return result["value__sum"]

    def get_spent_by_month(self, year: int, month: int) -> Decimal:
        """Посчитать, сколько потрачено на цель к году и месяцу

        Args:
            year (int): Год к которому надо посчитать
            month (int): Месяц к которому надо посчитать

        Returns:
            Decimal: Посчитанная сумма трат
        """

        last_day = monthrange(year, month)[1]
        result = GoalExpense.objects.filter(
            goal=self, date__lte=date(year=year, month=month, day=last_day)
        ).aggregate(Sum("value"))

        if not result["value__sum"]:
            return Decimal(0)
        return result["value__sum"]


class GoalExpense(models.Model):
    date = models.DateField(default=timezone.now)
    value = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal(0))
    percent = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal(0))
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date", "id"]

    def __str__(self) -> str:
        string = f"id: {self.id}, date: {self.date}"
        return string


class GoalBump(models.Model):
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    value = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal(0))

    class Meta:
        ordering = ["date", "id"]

    def __str__(self) -> str:
        string = f"id: {self.id}, date: {self.date}"
        return string
