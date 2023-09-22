from typing import List, Optional

from ddd.interfaces.agregates.outcomes.entities import Outcome


class IOutcomesRepo():
    def get_all_outcomes(self) -> Optional[List[Outcome]]:
        """Получить список всех расходов.

        Returns:
            Optional[List[Outcome]]: Список сущностей Расход.
        """
        raise NotImplementedError()