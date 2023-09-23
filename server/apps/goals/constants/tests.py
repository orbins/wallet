from decimal import Decimal
from typing import Final


class DefaultTestData:
    USER_DATA: Final[dict[str, str]] = {
        "email": "test@test.com",
        "username": "user",
        "password": "password"
    }

    INITIAL_BALANCE = 100000

    GOAL_CREATION_DATA_SET = [
        Decimal('1000'),
        Decimal('5000.99'),
        Decimal('18000.01'),
        Decimal('50000'),
        Decimal('249.50')
    ]

    TARGET_AMOUNT_DATA_SET = [
        Decimal('2000'),
        Decimal('10000.30'),
        Decimal('20000'),
        Decimal('60000'),
        Decimal('749.77')
    ]