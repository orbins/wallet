from decimal import Decimal

from django.db.models import QuerySet, Sum, DecimalField
from django.db.models.functions import Coalesce


class DepositQuerySet(QuerySet):

    def aggregate_amount(self) -> dict[str, Decimal]:
        return self.aggregate(
            total_amount=Coalesce(
                Sum(
                    'amount',
                ),
                0,
                output_field=DecimalField(),
            ),
        )
