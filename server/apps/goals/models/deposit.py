from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone, dateformat

from ..constants import DepositConstants


class Deposit(models.Model):
    goal = models.ForeignKey(
        to='goals.Goal',
        on_delete=models.CASCADE,
        related_name='deposits',
        verbose_name='Цель',
    )
    amount = models.DecimalField(
        decimal_places=2,
        validators=[
            MinValueValidator(DepositConstants.MIN_AMOUNT),
            MaxValueValidator(DepositConstants.MAX_AMOUNT),
        ],
        verbose_name='Сумма',
    )
    created_at = models.DateField(
        default=dateformat.format(timezone.nowe(), 'Y-m-d'),
        verbose_name='Дата пополнения',
    )

    class Meta:
        verbose_name = 'Пополнение'
        verbose_name_plural = 'Пополнения'
