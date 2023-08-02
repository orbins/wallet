from decimal import Decimal
from rest_framework import serializers

from ..constants import GoalError
from ..models import Deposit, Goal
from ...pockets.models import Transaction
from ..serializers import GoalRetrieveSerializer


class DepositRetrieveSerializer(serializers.ModelSerializer):
    goal = GoalRetrieveSerializer()

    class Meta:
        model = Deposit
        fields = ('id', 'goal', 'amount')


class DepositCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = ('id', 'goal', 'amount')

    def validate(self, attrs: dict) -> dict:
        goal = attrs['goal']
        if goal.is_completed:
            raise serializers.ValidationError(GoalError.CANT_REFILL_COMPLETE_GOAL)
        return attrs

    def validate_amount(self, amount: Decimal) -> Decimal:
        user = self.context['request'].user
        totals = Transaction.objects.filter(user=user).aggregate_totals()
        balance = totals['total_income'] - totals['total_expenses']
        if balance < amount:
            raise serializers.ValidationError(GoalError.BALANCE_LESS_AMOUNT)
        return amount

    def validate_goal(self, goal: Goal) -> Goal:
        user = self.context['request'].user

        if goal not in user.goals.all():
            raise serializers.ValidationError(GoalError.NOT_USERS_GOAL)
        else:
            return goal

    @property
    def data(self):
        return DepositRetrieveSerializer(instance=self.instance).data
