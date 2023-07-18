from django.db import models

from .managers import TransactionCategoryManager


class TransactionCategory(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Пользователь',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
    )

    objects = TransactionCategoryManager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_category_name')
        ]

    def __str__(self) -> str:
        return f'{self.name}'
