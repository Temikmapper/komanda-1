"""
Здесь хранятся базовые модели: траты и доходы, которые содержат общие методы
"""

from calendar import monthrange
from datetime import date
from decimal import Decimal
from django.db import models


class BaseContinousEntity:
    """Базовый класс для трат и доходов, они длятся во времени, могут накапливать в себе дочерние объекты"""

    _name_class: str = ""
    _url_name: str = ""
    _child_class: models.Model = None

    @classmethod
    def get_objects_in_month(cls, year: int, month: int) -> models.QuerySet:
        """Получить Queryset объектов, содержащих в месяце

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            models.QuerySet: Queryset из объектов этого типа
        """

        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)
        objects = cls.objects.filter(start_date__lte=first_date_in_month).filter(
            finish_date__gte=last_date_in_month
        )

        return objects

    @classmethod
    def get_sum_in_month(cls, year: int, month: int) -> Decimal:
        """Получить сумму для дочерних объектов в месяце

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            Decimal: Сумма за месяц
        """
        objects = cls.get_objects_in_month(year, month)
        print(objects.explain())

        result = Decimal(0)

        for item in objects:
            result += item.get_value_in_month(year, month)

        return result

    def get_absolute_url(self):
        return f"/{self._url_name}/constant/{self.id}"

    def get_edit_url(self):
        return f"/{self._url_name}/constant/{self.id}/edit"

    def get_bump_url(self):
        return f"/{self._url_name}/constant/{self.id}/bump"

    def get_delete_url(self):
        return f"/{self._url_name}/constant/{self.id}/delete"

    def get_children(self) -> models.QuerySet:
        """Получить дочерние объекты

        Returns:
            models.QuerySet: Queryset дочерних объектов
        """
        link = {f"{self._name_class}": self}
        return self._child_class.objects.filter(**link)

    def bump(self, value: Decimal, date: date) -> models.Model:
        """Увеличить значение родителя (добавить деньги)

        Args:
            value (Decimal): Сколько добавить
            date (date): Дата добавления

        Returns:
            models.Model: Объект
        """
        link = {f"{self._name_class}": self}
        return self._child_class.objects.create(date=date, value=value, **link)

    def get_value_in_month(self, year: int, month: int) -> Decimal:
        """Получить последнее значение в определённом месяце

        Args:
            year (int): Год
            month (int): Месяц

        Returns:
            int: Значение
        """
        first_date_in_month = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        last_date_in_month = date(year, month, last_day)

        # Если объект больше неактулен, то возвращаем 0
        if last_date_in_month > self.finish_date:
            return 0

        # Связь объекта с дочерними
        link = {f"{self._name_class}": self}

        history_items = self._child_class.objects.filter(**link)
        before_month = history_items.filter(date__lte=last_date_in_month)
        after_month = history_items.filter(date__gte=first_date_in_month)
        objects_in_month = before_month & after_month
        try:
            if len(objects_in_month) == 0:
                value = before_month.last().value
            else:
                value = objects_in_month.last().value
            return value
        except AttributeError:
            return 0

    def get_current_value(self) -> Decimal:
        """Получить последний дочерний объект

        Returns:
            models.Model: Дочерний объект
        """
        link = {f"{self._name_class}": self}
        return self._child_class.objects.filter(**link).last().value
