from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from rest_framework import serializers

from ..constants import TransactionTypes
from ..constants.errors import TransactionErrors
from .managers import TransactionManager


class Transaction(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Пользователь',
    )
    category = models.ForeignKey(
        to='pockets.TransactionCategory',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Категория',
        null=True,
    )
    transaction_date = models.DateField(
        verbose_name='Дата операции',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма операции',
        validators=(MinValueValidator(Decimal('0.01')),),
    )
    transaction_type = models.CharField(
        max_length=7,
        choices=TransactionTypes.CHOICES,
        verbose_name='Тип категории',
        null=True,
    )

    objects = TransactionManager()

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self) -> str:
        if self.transaction_type == 'income':
            return f'{self.transaction_type} {self.amount}'
        return f'{self.transaction_type} {self.category} {self.amount}'

    def save(self, *args, **kwargs):
        transaction_type = self.transaction_type
        category = self.category
        if transaction_type == TransactionTypes.INCOME and category:
            raise serializers.ValidationError(TransactionErrors.DOES_NOT_SET_CATEGORY)
        elif transaction_type == TransactionTypes.EXPENSE and not category:
            raise serializers.ValidationError(TransactionErrors.CATEGORY_NOT_SPECIFIED)
        return super().save(*args, **kwargs)
