from collections import OrderedDict

from rest_framework import serializers

from ..constants import TransactionErrors, TransactionTypes
from ..models import Transaction, TransactionCategory
from .transaction_category import CategorySerializer


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор получения операций"""
    category = CategorySerializer(required=False)

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transaction_date', 'amount', 'transaction_type')


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания операций"""
    category = serializers.PrimaryKeyRelatedField(
        queryset=TransactionCategory.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transaction_date', 'amount', 'transaction_type')

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context['request'].user

        if category and category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        else:
            return category

    def validate_transaction_type(self, transaction_type) -> Transaction.transaction_type:
        if transaction_type == TransactionTypes.PERCENTS:
            raise serializers.ValidationError(TransactionErrors.INCORRECT_TRANSACTION_TYPE)

        return transaction_type

    def validate(self, attrs: dict) -> dict:
        if self.instance:
            transaction_type = attrs.get('transaction_type', self.instance.transaction_type)
            category = attrs.get('category', self.instance.category)
        else:
            transaction_type = attrs['transaction_type']
            category = attrs.get('category', None)
        if transaction_type == TransactionTypes.INCOME and category:
            raise serializers.ValidationError(TransactionErrors.DOES_NOT_SET_CATEGORY)
        elif transaction_type == TransactionTypes.EXPENSE:
            if not category:
                raise serializers.ValidationError(TransactionErrors.CATEGORY_NOT_SPECIFIED)
            user = self.context['request'].user
            balance = Transaction.objects.filter(
                user=user
            ).calculate_balance()['balance']
            if balance < attrs['amount']:
                raise serializers.ValidationError(TransactionErrors.NOT_ENOUGH_BALANCE)
        return attrs

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
    """Сериализатор для общих данных"""
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)


class BalanceSerializer(serializers.Serializer):
    """Сериализатор для баланса"""
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
