from typing import Final


class DepositConstants:
    MIN_AMOUNT = 10.00
    MAX_AMOUNT = 300000.00


class RefillTypes:
    FROM_USER: Final[str] = 'от пользователя'
    FROM_PERCENTS: Final[str] = 'с процентов'

    CHOICES: Final[tuple[tuple[str, str], ...]] = (
        (FROM_USER, 'от пользователя'),
        (FROM_PERCENTS, 'с процентов'),
    )

    CHOICES_DICT: Final[dict[str, str]] = dict(CHOICES)
