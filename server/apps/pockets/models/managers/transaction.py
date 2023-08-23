from decimal import Decimal

from django.db.models import Manager

from ..querysets import TransactionQuerySet


class TransactionManager(Manager):
    def get_queryset(self, **kwargs) -> TransactionQuerySet:
        return TransactionQuerySet(
            self.model,
            using=self._db,
        )

    def aggregate_totals(self) -> dict[str, Decimal]:
        return self.get_queryset().aggregate_totals()

    def calculate_balance(self) -> dict[str, Decimal]:
        return self.get_queryset().calculate_balance()
