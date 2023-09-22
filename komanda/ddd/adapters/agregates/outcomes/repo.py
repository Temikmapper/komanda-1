from datetime import date
from decimal import Decimal
from typing import Dict, List
from ddd.interfaces.agregates.outcomes.entities import UsualOutcome
from ddd.interfaces.agregates.outcomes.repo import IOutcomesRepo
from ddd.interfaces.agregates.outcomes.value_objects import Category

from expenses import models


class OutcomesRepo(IOutcomesRepo):
    def create_usual_outcome(self, date: date, value: Decimal, category_id: int):
        models.UsualExpenses.objects.create(
            date=date,
            amount=value, 
            category_id=category_id,
        )

    def get_all_outcomes(self):
        objects = models.UsualExpenses.objects.all()
        objects = [object.as_entity for object in objects]
        return objects
    
    def get_outcome(self, id: int) -> UsualOutcome:
        object = models.UsualExpenses.objects.get(id=id)
        return object.as_entity
    
    def get_all_categories(self) -> List[Category]:
        objects = models.Categories.objects.all()
        objects = [object.as_entity for object in objects]
        return objects
    
    def get_categories_ids(self) -> List[str]:
        objects = models.Categories.objects.all().values_list('id', flat=True)
        return list(objects)
