from django_filters import rest_framework as filters

from ..models import TransactionCategory


class TransactionCategoryFilter(filters.FilterSet):
    month = filters.NumberFilter(field_name="transactions__transaction_date", lookup_expr="month")

    class Meta:
        model = TransactionCategory
        fields = ("month",)
