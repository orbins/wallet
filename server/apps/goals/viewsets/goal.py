from typing import Type

from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import viewsets, pagination, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..constants import RefillTypes, GoalConstants
from ..filters import GoalFilter
from ..models import Goal, Deposit
from ..serializers import (
    DepositCreateSerializer,
    GoalAnalyzeSerializer,
    GoalCompleteSerializer,
    GoalCreateSerializer,
    GoalRetrieveSerializer,
    GoalUpdateSerializer,
)
from ...pockets.constants import TransactionTypes
from ...pockets.models import Transaction


class GoalViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 5
    permission_classes = (IsAuthenticated,)
    filterset_class = GoalFilter
    SERIALIZER_CLASS_MAP = {
        'create': GoalCreateSerializer,
        'update': GoalUpdateSerializer,
        'partial_update': GoalUpdateSerializer,
        'destroy': GoalCreateSerializer,
        'retrieve': GoalRetrieveSerializer,
        'list': GoalRetrieveSerializer,
        'complete': GoalCompleteSerializer,
        'refill': DepositCreateSerializer,
        'analyze': GoalAnalyzeSerializer,
    }

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        return self.SERIALIZER_CLASS_MAP.get(
            self.action,
            GoalRetrieveSerializer
        )

    def get_queryset(self) -> QuerySet:
        queryset = Goal.objects.filter(
            user=self.request.user,
        ).order_by('-created_at')
        if self.action in ('list', 'retrieve'):
            queryset = queryset.annotate_with_days_to_goal(
            ).annotate_with_accumulated_amount()
        if self.action == 'top':
            queryset = queryset.filter(
                is_completed=False
            ).annotate_with_percentage_completion(
            ).order_by('-percentage_completion')[:GoalConstants.TOP_GOALS]

        return queryset

    def get_object(self) -> Goal:
        queryset = self.get_queryset()
        if self.action == 'analyze':
            obj = self.filter_queryset(queryset).get_analytical_data()
        else:
            obj = super().get_object()
        return obj

    def perform_create(self, serializer):
        user = self.request.user
        if self.action == 'refill':
            serializer.validated_data['refill_type'] = RefillTypes.FROM_USER
            instance = serializer.save()
            Transaction.objects.create(
                user=user,
                category=instance.goal.category,
                amount=instance.amount,
                transaction_type=TransactionTypes.EXPENSE,
                transaction_date=instance.created_at
            )
        else:
            instance = serializer.save(user=user)
            if instance.start_amount > 0:
                Deposit.objects.create(
                    goal=instance,
                    amount=instance.start_amount,
                    refill_type=RefillTypes.FROM_USER
                )
                Transaction.objects.create(
                    user=user,
                    category=instance.category,
                    amount=instance.start_amount,
                    transaction_type=TransactionTypes.EXPENSE,
                    transaction_date=instance.created_at
                )

    def perform_destroy(self, instance):
        if not instance.is_completed:
            user = self.request.user
            deposits_queryset = Deposit.objects.filter(goal=instance).aggregate_amount()
            accumulated_amount = deposits_queryset['total_amount']
            Transaction.objects.create(
                user=user,
                amount=accumulated_amount,
                transaction_type=TransactionTypes.INCOME,
                transaction_date=instance.created_at
            )
        instance.delete()

    def perform_update(self, serializer):
        serializer.save()
        if self.action == 'complete':
            user = self.request.user
            goal = self.get_object()
            deposit_queryset = Deposit.objects.filter(goal=goal).aggregate_amount()
            accumulated_amount = deposit_queryset['total_amount']
            Transaction.objects.create(
                user=user,
                amount=accumulated_amount,
                transaction_type=TransactionTypes.INCOME,
                transaction_date=timezone.now().date(),
            )

    @action(methods=('POST',), detail=False)
    def refill(self, request: Request, *args, **kwargs) -> Response:
        """Поплнение цели"""
        return super().create(request, *args, **kwargs)

    @action(methods=('PATCH',), detail=True)
    def complete(self, request: Request, *args, **kwargs) -> Response:
        """Завершение цели"""
        return super().partial_update(request, *args, **kwargs)

    @action(methods=('GET',), detail=False)
    def analyze(self, request: Request, *args, **kwargs) -> Response:
        """Общая статистика по целям"""
        return super().retrieve(request, *args, **kwargs)

    @action(methods=('GET',), detail=False)
    def top(self, request: Request, *args, **kwargs) -> Response:
        """Топ целей по завершенности"""
        return super().list(request, *args, **kwargs)
