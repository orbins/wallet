from django.db.models import QuerySet
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from ..models import TransactionCategory
from ..serializers import (
    TransactionCategorySerializer,
)


class TransactionCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get", "post",)
    serializer_class = TransactionCategorySerializer

    def get_queryset(self) -> QuerySet:
        queryset = TransactionCategory.objects.filter(
            user=self.request.user,
        ).annotate_with_transaction_sums().order_by(
            '-transactions_sum',
        )

        return queryset
