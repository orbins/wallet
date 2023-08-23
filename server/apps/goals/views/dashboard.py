from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..constants.deposit import RefillTypes
from ..models import Deposit
from ...pockets.serializers import CategoryRetrieveSerializer
from ...pockets.models import Transaction, TransactionCategory


class DashboardView(APIView):
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get']

    def get(self, request):
        transactions = Transaction.objects.filter(
            user=self.request.user,
            transaction_date__month=timezone.now().month
        ).aggregate_totals()

        category = TransactionCategory.objects.filter(
            user=self.request.user,
        ).annotate_with_transaction_sums(
        ).order_by(
            '-transactions_sum'
        ).first()

        data = {
            **transactions,

            'invested_amount_cur_month': Deposit.objects.filter(
                goal__user=self.request.user,
                refill_type=RefillTypes.FROM_USER,
                created_at__month=timezone.now().month
            ).aggregate_amount()['total_amount'],

            'most_expensive_category': CategoryRetrieveSerializer(
                category
            ).data if category else None
        }

        return Response(data)
