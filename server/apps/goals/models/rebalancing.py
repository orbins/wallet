from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Rebalancing(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name='Пользователь',
    )
    category = models.ForeignKey(
        to='goals.Goal',
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name='Категория',
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма',
        validators=(MinValueValidator(Decimal('0.01')),),
    )
    date = models.DateField(
        auto_now=True,
        verbose_name='Дата пополнения',
    )

    class Meta:
        verbose_name = 'Пополнение'
        verbose_name_plural = 'Пополнения'
