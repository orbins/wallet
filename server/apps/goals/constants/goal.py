from typing import Final


class GoalConstants:
    MIN_TERM = 1
    MAX_TERM = 99
    MIN_PERCENT = 0
    MAX_PERCENT = 100
    MIN_START_AMOUNT = 0
    MIN_TARGET_AMOUNT = 100


class GoalStatuses:
    IN_PROCESS: Final[str] = 'в процессе'
    COMPLETE: Final[str] = 'завершена'

    CHOICES: Final[tuple[tuple[str, str], ...]] = (
        (IN_PROCESS, 'процессе'),
        (COMPLETE, 'завершена'),
    )

    CHOICES_DICT: Final[dict[str, str]] = dict(CHOICES)
