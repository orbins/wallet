from typing import Final


class GoalError:
    TARGET_LESS_START: Final[str] = 'Начальная сумма не может быть больше целевой'
    BALANCE_LESS_AMOUNT: Final[str] = 'Вносимая сумма не может быть больше, чем баланс вашего счёта'
    NOT_USERS_GOAL: Final[str] = 'У пользователя нет такой цели'
    CANT_COMPLETE_GOAL: Final[str] = 'Невозможно завершить цель, пока накопленная сумма меньше целевой'
    GOAL_ALREADY_COMPLETE: Final[str] = 'Выбранная цель уже является выполненной'
