from decimal import Decimal
from typing import Type, Union

from django.utils import timezone
from rest_framework import viewsets, serializers, pagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import Transaction, TransactionCategory
from ..models.querysets import TransactionQuerySet
from ..serializers import (
    TransactionCategoryTransactionSumSerializer,
    TransactionCreateSerializer,
    TransactionRetrieveSerializer,
    TransactionGlobalSerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == 'total':
            serializer_class = TransactionGlobalSerializer
        elif self.action == 'expenses_by_category':
            serializer_class = TransactionCategoryTransactionSumSerializer
        elif self.action in {'create', 'update', 'partial_update'}:
            serializer_class = TransactionCreateSerializer
        else:
            serializer_class = TransactionRetrieveSerializer

        return serializer_class

    def get_queryset(self) -> TransactionQuerySet:
        if self.action == "expenses_by_category":
            queryset = TransactionCategory.objects.filter(
                user=self.request.user,
            ).annotate_with_transaction_sums()
        else:
            queryset = Transaction.objects.filter(
                user=self.request.user,
            ).select_related('category',).order_by(
                '-transaction_date', '-id',
            )
        return queryset

    def get_object(self) -> Union[Transaction, dict[str, Decimal]]:
        if self.action == 'total':
            current_month = timezone.now().month
            queryset = self.get_queryset().filter(transaction_date__month=current_month)
            obj = self.filter_queryset(queryset).aggregate_totals()
        else:
            obj = super().get_object()

        return obj

    @action(methods=('GET',), detail=False, url_path='global')
    def total(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='expenses-by-category')
    def expenses_by_category(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
