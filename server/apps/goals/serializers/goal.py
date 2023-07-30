from typing import OrderedDict

from rest_framework import serializers

from ..constants.errors import GoalError
from ..models import Goal, Deposit
from ...pockets.models import Transaction, TransactionCategory
from ...pockets.serializers import CategorySerializer
from ...pockets.constants import TransactionErrors


class GoalRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Goal
        fields = ('id', 'name', 'target_amount', 'start_amount', 'category', 'term', 'percent', 'status')


class GoalCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('id', 'name', 'target_amount', 'start_amount', 'category', 'term', 'percent')

    def validate(self, attrs: dict) -> dict:
        if self.instance:
            start_amount = attrs.get('start_amount', self.instance.start_amount)
            target_amount = attrs.get('target_amount', self.instance.target_amount)
        else:
            start_amount = attrs['start_amount']
            target_amount = attrs['target_amount']
        if self.context['view'].action in ('update', 'partial_update'):
            raise serializers.ValidationError(GoalError.CANT_CHANGE_START_AMOUNT)
        if start_amount > target_amount:
            raise serializers.ValidationError(GoalError.TARGET_LESS_START)
        user = self.context['request'].user
        totals = Transaction.objects.filter(user=user).aggregate_totals()
        balance = totals['total_income'] - totals['total_expenses']
        if balance < start_amount:
            raise serializers.ValidationError(GoalError.BALANCE_LESS_AMOUNT)
        return attrs

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context['request'].user

        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        return category

    @property
    def data(self) -> OrderedDict:
        return GoalRetrieveSerializer(instance=self.instance).data


class GoalCompleteSerializer(serializers.Serializer):

    def validate(self, attrs: dict) -> dict:
        user = self.context['request'].user
        goal = self.instance
        if goal not in user.goals.all():
            raise serializers.ValidationError(GoalError.NOT_USERS_GOAL)
        if goal.status:
            raise serializers.ValidationError(GoalError.GOAL_ALREADY_COMPLETE)
        deposit_queryset = Deposit.objects.filter(goal=goal).aggregate_amount()
        total_amount = deposit_queryset['total_amount']
        if total_amount < goal.target_amount:
            raise serializers.ValidationError(GoalError.CANT_COMPLETE_GOAL)
        goal.status = True
        return attrs

    @property
    def data(self):
        return GoalRetrieveSerializer(instance=self.instance).data
