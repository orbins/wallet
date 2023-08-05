from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..constants import RefillTypes, GoalConstants
from ..filters import GoalFilter
from ..models import Goal, Deposit
from ..serializers import (
    DepositCreateSerializer,
    GoalCompleteSerializer,
    GoalCreateSerializer,
    GoalRetrieveSerializer,
    GoalUpdateSerializer,
)
from ...pockets.constants import TransactionTypes
from ...pockets.models import Transaction, TransactionCategory


class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filterset_class = GoalFilter

    def get_serializer_class(self):
        if self.action == 'create':
            serializer = GoalCreateSerializer
        elif self.action in ('update', 'partial_update'):
            serializer = GoalUpdateSerializer
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
            Transaction.objects.create(
                user=user,
                category=instance.goal.category,
                amount=instance.amount,
                transaction_type=TransactionTypes.EXPENSE,
                transaction_date=instance.created_at
            )
        else:
            instance = serializer.save(user=user)
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
        user = self.request.user
        deposits_queryset = Deposit.objects.filter(goal=instance).aggregate_amount()
        total_amount = deposits_queryset['total_amount']
        instance.delete()
        Transaction.objects.create(
            user=user,
            amount=total_amount,
            transaction_type=TransactionTypes.INCOME,
            transaction_date=instance.created_at
        )

    def perform_update(self, serializer):
        user = self.request.user
        goal = self.get_object()
        serializer.save()
        deposit_queryset = Deposit.objects.filter(goal=goal).aggregate_amount()
        total_amount = deposit_queryset['total_amount']
        Transaction.objects.create(
            user=user,
            amount=total_amount,
            transaction_type=TransactionTypes.INCOME,
            transaction_date=timezone.now(),
        )

    @action(methods=('POST',), detail=False, url_path='refill')
    def refill_goal(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @action(methods=('PATCH',), detail=True, url_path='complete')
    def complete_goal(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='analytics')
    def analyze_goal(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()

        closest_goals = [goal.days_to_goal for goal in queryset.filter(is_completed=False) if goal.days_to_goal > 0]
        if len(closest_goals) > 0:
            closest_goals.sort()
            most_closest_goal = closest_goals[GoalConstants.CLOSEST_GOAL_INDEX]
        else:
            most_closest_goal = None

        categories = TransactionCategory.objects.filter(
            goals__in=queryset.filter(is_completed=True)
        ).annotate_with_goals_counter().order_by('goals_counter')
        if len(categories) > 0:
            most_successful_category = categories[1].name
        else:
            most_successful_category = None
        # INDEX

        categories = TransactionCategory.objects.filter(
            goals__in=queryset).annotate_with_goals_counter().order_by(
            'goals_counter')
        if len(categories) > 0:
            most_popular_category = categories[1].name
        else:
            most_popular_category = None
        # INDEX

        response = {
            'uncompleted_goals': queryset.count_uncompleted_goals(),

            'total_invested_amount': Deposit.objects.filter(
                goal__in=queryset.filter(is_completed=False)
            ).aggregate_amount()['total_amount'],

            'total_percent_amount': Deposit.objects.filter(
                goal__in=queryset,
                refill_type=RefillTypes.FROM_PERCENTS
            ).aggregate_amount()['total_amount'],

            'percent__amount_this_month': Deposit.objects.filter(
                refill_type=RefillTypes.FROM_PERCENTS,
                created_at__month=timezone.now().month
            ).aggregate_amount()['total_amount'],

            'most_closest_goal': most_closest_goal,
            'most_successful_category': most_successful_category,
            'most_popular_category': most_popular_category,

        }
        return Response(response)

