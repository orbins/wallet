from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..filters import TransactionCategoryFilter
from ..models import TransactionCategory
from ..serializers import (
    CategorySerializer,
    CategoryRetrieveSerializer,
)


class TransactionCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get", "post",)
    filterset_class = TransactionCategoryFilter

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == 'create':
            serializer_class = CategoryCreateSerializer
        else:
            serializer_class = CategoryRetrieveSerializer

        return serializer_class

    def get_queryset(self) -> QuerySet:
        queryset = TransactionCategory.objects.filter(
            user=self.request.user,
        ).annotate_with_transaction_sums().order_by(
            '-transactions_sum',
        )
        if self.action == "get_top":
            return queryset[:2]

        return queryset

    @action(methods=('GET',), detail=False, url_path='top-three')
    def get_top(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
