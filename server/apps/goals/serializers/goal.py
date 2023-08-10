import decimal
from decimal import Decimal
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
        fields = ('id', 'name', 'target_amount', 'start_amount',
                  'category', 'created_at', 'term', 'percent',
                  'is_completed', 'expire_date')


class GoalCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('id', 'name', 'target_amount', 'start_amount',
                  'category', 'term', 'percent')

    def validate(self, attrs: dict) -> dict:
        start_amount = attrs['start_amount']
        target_amount = attrs['target_amount']
        if start_amount > target_amount:
            raise serializers.ValidationError(GoalError.TARGET_LESS_START)
        return attrs

    def validate_start_amount(self, start_amount: Decimal) -> Decimal:
        user = self.context['request'].user
        totals = Transaction.objects.filter(user=user).aggregate_totals()
        balance = totals['total_income'] - totals['total_expenses']
        if balance < start_amount:
            raise serializers.ValidationError(GoalError.BALANCE_LESS_AMOUNT)
        return start_amount

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context['request'].user

        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        return category

    @property
    def data(self) -> OrderedDict:
        return GoalRetrieveSerializer(instance=self.instance).data


class GoalUpdateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if self.instance.is_completed:
            raise serializers.ValidationError(GoalError.CANT_UPDATE_COMPLETED)
        return attrs

    def validate_target_amount(self, target_amount: decimal.Decimal) -> decimal.Decimal:
        deposit_queryset = Deposit.objects.filter(goal=self.instance).aggregate_amount()
        accumulated_amount = deposit_queryset['total_amount']

        if accumulated_amount > target_amount:
            raise serializers.ValidationError(GoalError.TARGET_LESS_ACCUMULATED)

        return target_amount

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context['request'].user

        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        return category

    class Meta:
        model = Goal
        fields = ('id', 'name', 'target_amount',
                  'category', 'term', 'percent')

    @property
    def data(self):
        return GoalRetrieveSerializer(instance=self.instance).data


class GoalCompleteSerializer(serializers.Serializer):

    def validate(self, attrs: dict) -> dict:
        goal = self.instance
        if goal.is_completed:
            raise serializers.ValidationError(GoalError.GOAL_ALREADY_COMPLETE)

        deposit_queryset = Deposit.objects.filter(goal=self.instance).aggregate_amount()
        accumulated_amount = deposit_queryset['total_amount']

        if accumulated_amount < self.instance.target_amount:
            raise serializers.ValidationError(GoalError.NOT_ENOUGH_ACCUMULATED)

        return attrs

    @property
    def data(self):
        return GoalRetrieveSerializer(instance=self.instance).data

    def update(self, instance, validated_data):
        instance.is_completed = True
        instance.save()
        return instance


class GoalAnalyzeSerializer(serializers.Serializer):
    active_goals = serializers.IntegerField()
    most_closest_goal = serializers.IntegerField()
    total_active_balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    total_percents_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    percents_amount_cur_month = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    most_successful_category = CategorySerializer()
    most_popular_category = CategorySerializer()
