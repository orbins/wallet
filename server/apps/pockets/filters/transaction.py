from django_filters import rest_framework as filters

from ..models import Transaction


class TransactionFilter(filters.FilterSet):
    month = filters.NumberFilter(field_name="transaction_date", lookup_expr="month")
    year = filters.NumberFilter(field_name="transaction_date", lookup_expr="year")

    class Meta:
        model = Transaction
        fields = ("month", "year",)
