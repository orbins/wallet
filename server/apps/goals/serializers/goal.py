from typing import OrderedDict

from rest_framework import serializers

from ..constants.errors import GoalError
from ..models import Goal
from ...pockets.models import Transaction, TransactionCategory
from ...pockets.serializers import CategorySerializer
from ...pockets.constants import TransactionErrors


class GoalRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Goal
        fields = ('id', 'name', 'target_amount', 'start_amount', 'category', 'term', 'percent')


class GoalCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('id', 'name', 'target_amount', 'start_amount', 'category', 'term', 'percent')

    def validate(self, attrs: dict) -> dict:
        start_amount = attrs.get('start_amount', None)
        user = self.context['request'].user
        if start_amount:
            totals = Transaction.objects.filter(user=user).aggregate_totals()
            balance = totals['total_income'] - totals['total_expenses']
            if balance < start_amount:
                raise serializers.ValidationError(GoalError.BALANCE_LESS_START)
        return attrs

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context['request'].user

        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        else:
            return category

    @property
    def data(self) -> OrderedDict:
        return GoalRetrieveSerializer(instance=self.instance).data

    def update(self, instance: Goal, validated_data: dict) -> Goal:
        start_amount = validated_data.get('start_amount', instance.start_amount)
        target_amount = validated_data.get('target_amount', instance.target_amount)
        if start_amount > target_amount:
            raise serializers.ValidationError(GoalError.TARGET_LESS_START)
        return super().update(instance, validated_data)
