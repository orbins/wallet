import datetime
from django.db.models import QuerySet, F, ExpressionWrapper, DateField
from django.db.models.functions import TruncMonth
from django.utils import timezone, dateformat
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from ..filters import GoalFilter
from ..models import Goal, Deposit
from ..serializers import (
    GoalCreateSerializer, GoalRetrieveSerializer,
)
from ...pockets.models import Transaction


class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get", "post", "delete", "patch", "put")
    filterset_class = GoalFilter

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            serializer = GoalCreateSerializer
        else:
            serializer = GoalRetrieveSerializer

        return serializer

    def get_queryset(self) -> QuerySet:
        queryset = Goal.objects.filter(
            user=self.request.user,
        ).order_by("-date")

        order_by = self.request.query_params.get('order_by')
        if order_by in ('closest', 'further'):
            queryset = queryset.annotate(
                completion=TruncMonth('date') + ExpressionWrapper(
                    datetime.timedelta(days=30) * F('term'), output_field=DateField())
            )

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save(user=user)
        amount = instance.start_amount
        category = instance.category
        Deposit.objects.create(
            user=user,
            goal=instance,
            amount=amount
        )
        Transaction.objects.create(
            user=user,
            category=category,
            amount=amount,
            transaction_type="expense",
            transaction_date=dateformat.format(timezone.now(), 'Y-m-d')
        )

    def perform_destroy(self, instance):
        user = self.request.user
        amount = instance.start_amount
        instance.delete()
        Transaction.objects.create(
            user=user,
            amount=amount,
            transaction_type="income",
            transaction_date=dateformat.format(timezone.now(), 'Y-m-d')
        )
