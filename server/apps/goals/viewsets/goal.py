from django.utils import timezone, dateformat
from django.db.models import QuerySet
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from ..models import Goal, Deposit
from ..serializers import (
    GoalCreateSerializer, GoalRetrieveSerializer,
)
from ...pockets.models import Transaction


class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get", "post", "delete", "patch", "put")

    def get_serializer_class(self):
        if self.action == 'create':
            serializer = GoalCreateSerializer
        else:
            serializer = GoalRetrieveSerializer

        return serializer

    def get_queryset(self) -> QuerySet:
        queryset = Goal.objects.filter(
            user=self.request.user,
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
