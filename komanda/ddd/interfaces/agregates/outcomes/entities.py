from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ddd.interfaces.agregates.outcomes.value_objects import Category


@dataclass
class Outcome:
    uuid: UUID
    datetime: datetime
    value: Decimal


@dataclass
class UsualOutcome:
    id: int
    """ID в БД, пока не перенесено на UUID."""
    uuid: UUID
    outcome: Outcome
    category: Category


@dataclass
class GoalOutcome:
    uuid: UUID
    outcome: Outcome