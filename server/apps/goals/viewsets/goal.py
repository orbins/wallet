from django.db.models import QuerySet
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from ..filters import GoalFilter
from ..models import Goal, Deposit
from ...pockets.constants import TransactionTypes
from ...pockets.models import Transaction
from ..serializers import (
    GoalCreateSerializer, GoalRetrieveSerializer,
)
from ..services import get_deposits_sum


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
        ).order_by("-created_at")

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save(user=user)
        amount = instance.start_amount
        category = instance.category
        created_at = instance.created_at
        Deposit.objects.create(
            goal=instance,
            amount=amount
        )
        Transaction.objects.create(
            user=user,
            category=category,
            amount=amount,
            transaction_type=TransactionTypes.EXPENSE,
            transaction_date=created_at
        )

    def perform_destroy(self, instance):
        user = self.request.user
        deposits_amount = get_deposits_sum(instance.id)
        total_amount = instance.start_amount + deposits_amount
        created_at = instance.created_at
        instance.delete()
        Transaction.objects.create(
            user=user,
            amount=total_amount,
            transaction_type=TransactionTypes.INCOME,
            transaction_date=created_at
        )
