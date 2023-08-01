from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..constants import RefillTypes
from ..filters import GoalFilter
from ..models import Goal, Deposit
from ...pockets.constants import TransactionTypes
from ...pockets.models import Transaction
from ..serializers import (
    DepositCreateSerializer,
    GoalCompleteSerializer,
    GoalCreateSerializer,
    GoalRetrieveSerializer,
)


class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filterset_class = GoalFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            serializer = GoalCreateSerializer
        elif self.action == 'refill_goal':
            serializer = DepositCreateSerializer
        elif self.action == 'complete_goal':
            serializer = GoalCompleteSerializer
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
        if self.action == 'refill_goal':
            instance = serializer.save()
            category = instance.goal.category
            amount = instance.amount
            created_at = instance.created_at
            Transaction.objects.create(
                user=user,
                category=category,
                amount=amount,
                transaction_type=TransactionTypes.EXPENSE,
                transaction_date=created_at
            )
        else:
            instance = serializer.save(user=user)
            amount = instance.start_amount
            created_at = instance.created_at
            category = instance.category
            Deposit.objects.create(
                goal=instance,
                amount=amount,
                refill_type=RefillTypes.FROM_USER
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
        deposits_queryset = Deposit.objects.filter(goal=instance).aggregate_amount()
        total_amount = deposits_queryset['total_amount']
        created_at = instance.created_at
        instance.delete()
        Transaction.objects.create(
            user=user,
            amount=total_amount,
            transaction_type=TransactionTypes.INCOME,
            transaction_date=created_at
        )

    def perform_update(self, serializer):
        if self.action == 'complete_goal':
            user = self.request.user
            goal = self.get_object()
            deposit_queryset = Deposit.objects.filter(goal=goal).aggregate_amount()
            total_amount = deposit_queryset['total_amount']
            Transaction.objects.create(
                user=user,
                amount=total_amount,
                transaction_type=TransactionTypes.INCOME,
                transaction_date=timezone.now(),
            )
        else:
            serializer.save()

    @action(methods=('POST',), detail=False, url_path='refill')
    def refill_goal(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @action(methods=('PATCH',), detail=True, url_path='complete')
    def complete_goal(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)
