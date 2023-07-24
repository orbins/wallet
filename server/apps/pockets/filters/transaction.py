from django_filters import rest_framework as filters

from ..models import Transaction


class TransactionFilter(filters.FilterSet):
    month = filters.NumberFilter(field_name="transaction_date", lookup_expr="month")
    year = filters.NumberFilter(field_name="transaction_date", lookup_expr="year")
    order_by = filters.OrderingFilter(
        fields=(
            ('transaction_date', 'date'),
            ('amount', 'amount'),
            ('category', 'category'),
        )
    )

    class Meta:
        model = Transaction
        fields = ("month", "year",)
