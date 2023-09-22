from datetime import date
from decimal import Decimal
from typing import Dict
from ddd.adapters.agregates.outcomes.repo import OutcomesRepo
from ddd.adapters.operations.usual_outcomes.use_cases import ValidateOutcomeDataUseCase
from ddd.arch.base import Command


class CreateOutcomeCommand(Command):
    def __init__(self) -> None:
        super().__init__()
        self.repo = OutcomesRepo()
        self._validate_data = ValidateOutcomeDataUseCase()

    def execute(self, data: Dict) -> None:
        self._validate_data(data)
        _date = date.fromisoformat(data["date"])
        value = Decimal(data["amount"])
        category_id = int(data["category_id"])

        self.repo.create_usual_outcome(date=_date, value=value, category_id=category_id)


class GetAllCategoriesCommand(Command):
    def __init__(self) -> None:
        super().__init__()
        self.repo = OutcomesRepo()

    def execute(self) -> None:
        all_categories = self.repo.get_all_categories()
        self.events.append(all_categories)


class GetAllOutcomesCommand(Command):
    def __init__(self) -> None:
        super().__init__()
        self.repo = OutcomesRepo()

    def execute(self):
        all_outcomes = self.repo.get_all_outcomes()
        self.events.append(all_outcomes)


class GetUsualOutcomeCommand(Command):
    def __init__(self) -> None:
        super().__init__()
        self.repo = OutcomesRepo()

    def execute(self, id: int) -> None:
        outcome = self.repo.get_outcome(id)
        self.events.append(outcome)
