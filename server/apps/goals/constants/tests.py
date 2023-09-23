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
        (Decimal('765.20'), Decimal('5000'), 5, Decimal('765.30')),
        (Decimal('28694.33'), Decimal('100000'), 15, Decimal('28706.12')),
        (Decimal('5000'), Decimal('27500'), 7, Decimal('5000.96')),
        (Decimal('55750'), Decimal('70000'), 10, Decimal('55765.27')),
        (Decimal('44692.50'), Decimal('48000'), 8, Decimal('44702.30')),
    ]
