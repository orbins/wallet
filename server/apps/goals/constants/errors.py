from typing import Final


class GoalError:
    TARGET_LESS_START: Final[str] = 'Начальная сумма не может быть больше целевой'
    BALANCE_LESS_AMOUNT: Final[str] = 'Вносимая сумма не может быть больше, чем баланс вашего счёта'
    NOT_USERS_GOAL: Final[str] = 'У пользователя нет такой цели'
    GOAL_ALREADY_COMPLETE: Final[str] = 'Выбранная цель уже является выполненной'
    CANT_CHANGE_START_AMOUNT: Final[str] = 'Нельзя изменить стартовую сумму'
    CANT_REFILL_COMPLETE_GOAL: Final[str] = 'Эта цель уже выполнена, вы не можете её пополнить'
    TARGET_LESS_ACCUMULATED: Final[str] = 'Целевая сумма не может быть меньше накопленной'
    NOT_ENOUGH_ACCUMULATED: Final[str] = 'Не достаточно средств для завершения цели'
