from decimal import Decimal
from typing import Final


class GoalConstants:
    MIN_TERM: Final[int] = 1
    MIN_PERCENT: Final[int] = 0
    MAX_PERCENT: Final[int] = 100
    MIN_START_AMOUNT: Final[Decimal] = Decimal('0')
    MIN_TARGET_AMOUNT: Final[Decimal] = Decimal('0.01')
    CLOSEST_GOAL_INDEX: Final[int] = 0
    TOP_GOALS = 3
