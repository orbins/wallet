from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework import serializers

from ..constants import GoalError


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
        null=True,
    )
    date = models.DateField(
        auto_now=True,
        verbose_name='Дата создания',
    )
    term = models.IntegerField(
        verbose_name='Срок',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99),
        ]
    )
    target_amount = models.IntegerField(
        verbose_name='Целевая сумма',
        validators=[
            MinValueValidator(100),
        ],
    )
    start_amount = models.IntegerField(
        verbose_name='Начальная сумма',
        validators=[
            MinValueValidator(0),
        ],
    )
    percent = models.IntegerField(
        verbose_name='Процент',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def save(self, *args, **kwargs):
        if self.start_amount > self.target_amount:
            raise serializers.ValidationError(GoalError.TARGET_LESS_START)
        return super().save(*args, **kwargs)
