from decimal import Decimal

from django.db.models import Manager

from ..querysets import DepositQuerySet


class DepositManager(Manager):
    def get_queryset(self, **kwargs) -> DepositQuerySet:
        return DepositQuerySet(
            self.model,
            using=self._db,
        )

    def aggregate_amount(self) -> dict[str, Decimal]:
        return self.get_queryset().aggregate_amount()
