import datetime

from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .managers import GoalManager
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
        default=datetime.date.today,
        verbose_name='Дата создания',
    )
    term = models.PositiveIntegerField(
        verbose_name='Срок',
        validators=[
            MinValueValidator(GoalConstants.MIN_TERM),
        ]
    )
    expire_date = models.DateField(
        verbose_name='Дата окончания срока',
        null=True
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
    is_completed = models.BooleanField(
        default=False,
        verbose_name='статус',
    )

    objects = GoalManager()

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        unique_together = ['user', 'name']

    def save(self, *args, **kwargs):
        if not self.expire_date:
            self.expire_date = self.created_at + relativedelta(months=self.term)
        super().save(*args, **kwargs)

    # @property
    # def accumulated_amount(self):
    #     queryset = Deposit.objects.filter(goal=self)
    #     accumulated_amount = queryset.aggregate_amount()['total_amount']
    #     return accumulated_amount

    # @property
    # def percent_amount(self):
    #     queryset = Deposit.objects.filter(goal=self, refill_type=RefillTypes.FROM_PERCENTS)
    #     percent_amount = queryset.aggregate_amount()['total_amount']
    #     return percent_amount
