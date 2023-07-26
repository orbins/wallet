from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone, dateformat
from rest_framework import serializers

from ..constants import GoalError, GoalConstants


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
    start_amount = models.DecimalField(
        verbose_name='Начальная сумма',
        validators=[
            MinValueValidator(GoalConstants.MIN_START_AMOUNT),
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

    def save(self, *args, **kwargs):
        if self.start_amount > self.target_amount:
            raise serializers.ValidationError(GoalError.TARGET_LESS_START)
        return super().save(*args, **kwargs)
