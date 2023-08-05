from django.db.models import QuerySet, Sum, Count, DecimalField, IntegerField
from django.db.models.functions import Coalesce


class TransactionCategoryQuerySet(QuerySet):
    def annotate_with_transaction_sums(self):
        """
        :return: TransactionCategoryQuerySet
        """

        return self.annotate(
            transactions_sum=Coalesce(
                Sum('transactions__amount'),
                0,
                output_field=DecimalField(),
            ),
        )

    def annotate_with_goals_counter(self):
        """
        :return: TransactionCategoryQuerySet
        """

        return self.annotate(
            goals_counter=Coalesce(
                Count('goals'),
                None,
                output_field=IntegerField(),
            ),
        )
