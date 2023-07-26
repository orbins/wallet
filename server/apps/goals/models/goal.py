from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone, dateformat

from ..constants import GoalConstants


class Goal(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name='Пользователь',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
    )
    category = models.ForeignKey(
        to='pockets.TransactionCategory',
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name='Категория',
    )
    created_at = models.DateField(
        default=dateformat.format(timezone.nowe(), 'Y-m-d'),
        verbose_name='Дата создания',
    )
    term = models.PositiveIntegerField(
        verbose_name='Срок',
        validators=[
            MinValueValidator(GoalConstants.MIN_TERM),
        ]
    )
    target_amount = models.DecimalField(
        verbose_name='Целевая сумма',
        validators=[
            MinValueValidator(GoalConstants.MIN_TARGET_AMOUNT),
        ],
    )
    accumulated_amount = models.DecimalField(
        verbose_name='Накопленная сумма',
        validators=[
            MinValueValidator(GoalConstants.MIN_ACCUMULATED_AMOUNT),
        ],
    )
    percent = models.PositiveIntegerField(
        verbose_name='Процент',
        validators=[
            MinValueValidator(GoalConstants.MIN_PERCENT),
            MaxValueValidator(GoalConstants.MAX_PERCENT),
        ],
    )

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        unique_together = ['user', 'name']
