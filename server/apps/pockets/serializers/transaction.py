from collections import OrderedDict

from rest_framework import serializers

from ..constants import TransactionErrors, TransactionTypes
from ..models import Transaction, TransactionCategory
from .transaction_category import CategorySerializer


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transaction_date', 'amount', 'transaction_type')


class TransactionCreateSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(
        choices=TransactionTypes.CHOICES,
    )

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transaction_date', 'amount', 'transaction_type')

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context['request'].user

        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        else:
            return category

    def create(self, validated_data: dict) -> Transaction:
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    @property
    def data(self) -> OrderedDict:
        """
        Сделано для того, чтобы при создании объекта можно было передвавть id категории, а после
        создания поле категории возвращалось как объект
        """
        return TransactionRetrieveSerializer(instance=self.instance).data


class TransactionGlobalSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)


class ExpenseCategoryTransactionSumSerializer(serializers.ModelSerializer):
    transactions_sum = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj["category__name"]

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transactions_sum')


class BalanceSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
