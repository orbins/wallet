from django.db.models import QuerySet, Sum, Count, DecimalField, IntegerField
from django.db.models.functions import Coalesce

from ...constants import TOP_CATEGORIES


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

    def get_top_with_others(self):
        data = list(self[:TOP_CATEGORIES])
        other_categories_amount = self[TOP_CATEGORIES:].aggregate(
            total_amount=Sum('transactions_sum')
        )['total_amount'] or 0
        data.append(
            {
                'id': None,
                'name': 'другое',
                'transactions_sum': other_categories_amount
            }
        )

        return data
