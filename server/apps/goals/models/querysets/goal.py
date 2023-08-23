import decimal

from django.db.models import (
    QuerySet, F, Q,
    PositiveIntegerField, DecimalField,
    Sum, Count
)
from django.db.models.functions import Coalesce, ExtractDay
from django.utils import timezone


from ...constants import RefillTypes
from ....pockets.models import TransactionCategory


class GoalQuerySet(QuerySet):

    def annotate_with_days_to_goal(self) -> QuerySet:
        return self.annotate(
            days_to_goal=Coalesce(
                ExtractDay(F('expire_date') - timezone.now().date()),
                0,
                output_field=PositiveIntegerField()
            )
        )

    def annotate_with_accumulated_amount(self) -> QuerySet:
        return self.annotate(
            accumulated_amount=Coalesce(
                Sum('deposits__amount'),
                0,
                output_field=DecimalField()
            ),
            accumulated_amount_cur_month=Coalesce(
                Sum(
                    'deposits__amount',
                    filter=Q(
                        deposits__created_at__month=timezone.now().month,
                        deposits__created_at__year=timezone.now().year
                    )
                ),
                0,
                output_field=DecimalField()
            )
        )

    def total_active_balance(self):
        return self.aggregate(
            total_active_balance=Coalesce(
                Sum(
                    'deposits__amount',
                    filter=Q(is_completed=False)
                    ),
                0,
                output_field=DecimalField()
            )
        )

    def percents_amount(self):
        return self.aggregate(
            total_percents_amount=Coalesce(
                Sum(
                    'deposits__amount',
                    filter=Q(
                        deposits__refill_type=(
                            RefillTypes.FROM_PERCENTS
                        )
                    )
                ),
                0,
                output_field=DecimalField()
            ),
            percents_amount_cur_month=Coalesce(
                Sum(
                    'deposits__amount',
                    filter=Q(
                        deposits__refill_type=(
                            RefillTypes.FROM_PERCENTS
                        ),
                        created_at__month=timezone.now().month
                    )
                ),
                0,
                output_field=DecimalField()
            )
        )

    def get_most_popular_category(self):
        obj = self.values('category').annotate(
            goal_count=Count('id')
        ).order_by('-goal_count').first()

        return obj['category'] if obj else None

    def get_most_successful_category(self):
        obj = self.filter(
            is_completed=True,
        ).values(
            'category'
        ).annotate(
            goal_count=Count('id')
        ).order_by(
            '-goal_count'
        ).first()

        return obj['category'] if obj else None

    def get_analytical_data(self):
        most_closest_goal = self.filter(
            is_completed=False
        ).annotate_with_days_to_goal().order_by(
            'days_to_goal'
        ).first()
        most_popular_category = self.get_most_popular_category()
        most_successful_category = self.get_most_successful_category()

        data = {
            'active_goals': self.filter(is_completed=False).count(),

            'most_closest_goal': most_closest_goal.days_to_goal if most_closest_goal else None,

            **self.total_active_balance(),
            **self.percents_amount(),

            'most_popular_category': TransactionCategory.objects.get(
                id=most_popular_category
            ) if most_popular_category else None,

            'most_successful_category': TransactionCategory.objects.get(
                id=most_successful_category
            ) if most_successful_category else None

        }

        return data

    def annotate_with_percentage_completion(self):
        return self.annotate(
            percentage_completion=Coalesce(
                Sum('deposits__amount') / F('target_amount') * 100,
                0,
                output_field=PositiveIntegerField(),
            )
        )
