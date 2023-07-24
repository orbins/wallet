from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Deposit(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='deposits',
        verbose_name='Пользователь',
    )
    goal = models.ForeignKey(
        to='goals.Goal',
        on_delete=models.CASCADE,
        related_name='deposits',
        verbose_name='Цель',
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(10),
            MaxValueValidator(300000),
        ],
        verbose_name='Сумма',
    )
    date = models.DateField(
        auto_now=True,
        verbose_name='Дата пополнения',
    )

    class Meta:
        verbose_name = 'Пополнение'
        verbose_name_plural = 'Пополнения'
