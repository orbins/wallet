from ..models import Deposit


def get_deposits_sum(goal):
    amount_list = Deposit.objects.values_list('amount').filter(goal=goal)
    total_amount = sum(amount_list)
    return total_amount

