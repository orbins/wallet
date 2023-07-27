from typing import Final


class GoalError:
    TARGET_LESS_START: Final[str] = 'Начальная сумма не может быть больше целевой'
    BALANCE_LESS_START: Final[str] = 'Вносимая сумма не может быть больше, чем баланс вашего счёта'
