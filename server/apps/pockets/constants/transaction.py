from typing import Final


class TransactionTypes:
    INCOME: Final[str] = 'income'
    EXPENSE: Final[str] = 'expense'
    PERCENTS: Final[str] = 'percents'

    CHOICES: Final[tuple[tuple[str, str], ...]] = (
        (INCOME, 'Доход'),
        (EXPENSE, 'Расход'),
        (PERCENTS, 'Проценты')
    )

    CHOICES_DICT: Final[dict[str, str]] = dict(CHOICES)


TOP_CATEGORIES = 3
