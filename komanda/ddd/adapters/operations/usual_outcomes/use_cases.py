from typing import Any, Dict
from ddd.adapters.agregates.outcomes.repo import OutcomesRepo

from ddd.interfaces.agregates.outcomes.entities import UsualOutcome, Outcome


class ValidateOutcomeDataUseCase():
    def __init__(self) -> None:
        self.repo = OutcomesRepo()

    def __call__(self, data: Dict) -> None:
        categories_list = self.repo.get_categories_ids()
        if int(data["category_id"]) not in categories_list:
            raise TypeError()
