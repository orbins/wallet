from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from .managers import DepositManager
from ..constants import DepositConstants, RefillTypes


class Deposit(models.Model):
    """Модель вложений в цель"""
    goal = models.ForeignKey(
        to='goals.Goal',
        on_delete=models.CASCADE,
        related_name='deposits',
        verbose_name='Цель',
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        validators=[
            MinValueValidator(DepositConstants.MIN_AMOUNT),
            MaxValueValidator(DepositConstants.MAX_AMOUNT),
        ],
        verbose_name='Сумма',
    )
    created_at = models.DateField(
        default=timezone.now,
        verbose_name='Дата пополнения',
    )
    refill_type = models.CharField(
        max_length=15,
        choices=RefillTypes.CHOICES,
        verbose_name='Тип пополнения',
    )

    objects = DepositManager()

    class Meta:
        verbose_name = 'Пополнение'
        verbose_name_plural = 'Пополнения'
