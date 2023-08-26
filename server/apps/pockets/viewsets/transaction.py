from decimal import Decimal
from typing import Type, Union

from django.http import HttpResponse, FileResponse
from openpyxl import Workbook
from rest_framework import viewsets, serializers, pagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..filters import TransactionFilter
from ..models import Transaction
from ..models.querysets import TransactionQuerySet
from ..serializers import (
    BalanceSerializer,
    TransactionCreateSerializer,
    TransactionRetrieveSerializer,
    TransactionGlobalSerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (IsAuthenticated,)
    filterset_class = TransactionFilter

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == 'total':
            serializer_class = TransactionGlobalSerializer
        elif self.action == 'get_balance':
            serializer_class = BalanceSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            serializer_class = TransactionCreateSerializer
        else:
            serializer_class = TransactionRetrieveSerializer

        return serializer_class

    def get_queryset(self) -> TransactionQuerySet:
        queryset = Transaction.objects.filter(
            user=self.request.user,
        ).select_related('category',).order_by(
            '-transaction_date', '-id',
        )
        return queryset

    def get_object(self) -> Union[Transaction, dict[str, Decimal]]:
        queryset = self.get_queryset()
        if self.action == 'total':
            obj = self.filter_queryset(queryset).aggregate_totals()
        elif self.action == 'get_balance':
            obj = self.filter_queryset(queryset).calculate_balance()
        else:
            obj = super().get_object()

        return obj

    @action(methods=('GET',), detail=False, url_path='global')
    def total(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='balance')
    def get_balance(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(methods=('GET',), detail=False)
    def export(self, request: Request, *args, **kwargs) -> FileResponse:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{request.user.username}.xlsx"'

        transactions = self.get_queryset().only(
            'category', 'transaction_date',
            'amount', 'transaction_type'
        )

        wb = Workbook()
        ws = wb.active
        ws.title = f'Операции'
        headers = ['Дата операции', 'Тип операции', 'Категория', 'Сумма']
        ws.append(headers)
        for instance in transactions:
            data = [
                instance.transaction_date,
                'Доход' if instance.transaction_type == 'income' else 'Расход',
                instance.category.name if instance.category else None,
                instance.amount
            ]
            ws.append(data)
        wb.save(response)

        return response



