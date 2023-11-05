from django.db import models


class Quote(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='quotes',
        verbose_name='Пользователь',
    )
    text = models.TextField(
        verbose_name='Текст',
    )

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'
