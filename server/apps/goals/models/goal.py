from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from ..constants import GoalConstants, GoalStatuses


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
        default=timezone.now,
        verbose_name='Дата создания',
    )
    term = models.PositiveIntegerField(
        verbose_name='Срок',
        validators=[
            MinValueValidator(GoalConstants.MIN_TERM),
        ]
    )
    target_amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name='Целевая сумма',
        validators=[
            MinValueValidator(GoalConstants.MIN_TARGET_AMOUNT),
        ],
    )
    start_amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name='Накопленная сумма',
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
    status = models.BooleanField(
        default=False,
        verbose_name='статус',
    )

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        unique_together = ['user', 'name']

    @property
    def expire_date(self):
        return self.created_at + relativedelta(months=self.term)
