from decimal import Decimal

from django.db.models import QuerySet, Sum, Q, DecimalField
from django.db.models.functions import Coalesce

from ...constants import TransactionTypes


class TransactionQuerySet(QuerySet):

    def aggregate_totals(self) -> dict[str, Decimal]:
        """
        Возвращает общие доходы, расходы и проценты,
        начисленные на цели
        """
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
            total_percents=Coalesce(
                Sum(
                    'amount',
                    filter=Q(transaction_type=TransactionTypes.PERCENTS),
                ),
                0,
                output_field=DecimalField(),
            ),

        )

    def calculate_balance(self) -> dict[str, Decimal]:
        """Подсчитывает текущий баланс пользователя"""
        return self.aggregate(
            balance=
            Coalesce(
                Sum(
                    'amount',
                    filter=Q(transaction_type=TransactionTypes.INCOME),
                ),
                0,
                output_field=DecimalField(),
            ) -
            Coalesce(
                Sum(
                    'amount',
                    filter=Q(transaction_type=TransactionTypes.EXPENSE),
                ),
                0,
                output_field=DecimalField(),
            ) -
            Coalesce(
                Sum(
                    'amount',
                    filter=Q(transaction_type=TransactionTypes.PERCENTS),
                ),
                0,
                output_field=DecimalField(),
            ),
        )
