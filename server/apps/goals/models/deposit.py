from django.core.validators import MinValueValidator
from django.db import models


class Deposit(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='deposits',
        verbose_name='Пользователь',
    )
    category = models.ForeignKey(
        to='goals.Goal',
        on_delete=models.CASCADE,
        related_name='deposits',
        verbose_name='Категория',
        null=True,
    )
    amount = models.IntegerField(
        verbose_name='Сумма',
        validators=[
            MinValueValidator(100),
        ],
    ),
    date = models.DateField(
        auto_now=True,
        verbose_name='Дата пополнения',
    )

    class Meta:
        verbose_name = 'Пополнение'
        verbose_name_plural = 'Пополнения'
