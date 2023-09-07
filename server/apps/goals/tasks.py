import decimal

from celery import shared_task
from django.utils import timezone

from .constants import RefillTypes
from .models import Deposit, Goal
from ..pockets.models import Transaction
from ..pockets.constants import TransactionTypes


@shared_task
def calculate_daily_percent():
    """
    Начисляет проценты на все незавершенные цели
    всех пользователей
    """
    goals = Goal.objects.filter(is_completed=False)
    for goal in goals:
        deposit_queryset = Deposit.objects.filter(goal=goal).aggregate_amount()
        accumulated_amount = deposit_queryset['total_amount']
        daily_percent = (accumulated_amount/100) * decimal.Decimal(goal.percent/365)
        Deposit.objects.create(
            goal=goal,
            amount=daily_percent,
            refill_type=RefillTypes.FROM_PERCENTS
        )
        Transaction.objects.create(
            user=goal.user,
            amount=daily_percent,
            transaction_type=TransactionTypes.PERCENTS,
            transaction_date=timezone.now().date(),
        )
