from decimal import Decimal
from typing import Final


class DefaultTestData:
    USER_DATA: Final[dict[str, str]] = {
        "email": "test@test.com",
        "username": "user",
        "password": "password"
    }

    INITIAL_BALANCE = 200000

    START_AMOUNT_DATA_SET = [
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

    GOAL_CREATION_DATA_SET = [
        (Decimal('765.20'), 5, Decimal('765.30')),
        (Decimal('28694.33'), 15, Decimal('28706.12')),
        (Decimal('5000'), 7, Decimal('5000.96')),
        (Decimal('55750'), 10, Decimal('55765.27')),
        (Decimal('44692.50'), 8, Decimal('44702.30')),
    ]

    TARGET_AMOUNT_FOR_PERCENTS = 100000
