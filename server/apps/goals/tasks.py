from celery import shared_task

from .constants import RefillTypes
from .models import Deposit, Goal


@shared_task
def calculate_daily_percent():
    goals = Goal.objects.filter(is_completed=False)
    for goal in goals:
        deposit_queryset = Deposit.objects.filter(goal=goal).aggregate_amount()
        total_amount = deposit_queryset['total_amount']
        daily_percent = (total_amount/100) * (goal.term/365)
        Deposit.objects.create(
            goal=goal,
            amount=daily_percent,
            refill_type=RefillTypes.FROM_PERCENTS
        )
