from decimal import Decimal

from django.db.models import QuerySet, Sum, Q, DecimalField
from django.db.models.functions import Coalesce

from ...constants import TransactionTypes


class TransactionQuerySet(QuerySet):

    def aggregate_totals(self) -> dict[str, Decimal]:
        return self.aggregate(
            total_income=Coalesce(
                Sum(
                    'amount',
                    filter=Q(transaction_type=TransactionTypes.INCOME),
                ),
                0,
                output_field=DecimalField(),
            ),
            total_expenses=Coalesce(
                Sum(
                    'amount',
                    filter=Q(transaction_type=TransactionTypes.EXPENSE),
                ),
                0,
                output_field=DecimalField(),
            ),
        )

    def annotate_category_expenses(self):
        return self.values("category__name").annotate(
            transactions_sum=Coalesce(
                Sum('amount'),
                0,
                output_field=DecimalField(),
            ),
        )
