from decimal import Decimal

from django.db.models import QuerySet, Sum, Q, DecimalField
from django.db.models.functions import Coalesce


class TransactionQuerySet(QuerySet):

    def aggregate_deposits_amount(self) -> dict[str, Decimal]:
        return self.aggregate(
            total_amount=Coalesce(
                Sum(
                    'amount',
                ),
                0,
                output_field=DecimalField(),
            ),
        )
