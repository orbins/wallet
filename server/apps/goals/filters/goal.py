from django_filters import rest_framework as filters


class GoalFilter(filters.FilterSet):

    order_by = filters.OrderingFilter(
        fields=(
            ('-percent', 'higher_percent'),
            ('percent', 'lower_percent'),
            ('-target_amount', 'most_expensive'),
            ('target_amount', 'cheapest'),
            ('created_at', 'newest'),
            ('-created_at', 'oldest'),
            ('expire_date', 'closest'),
            ('-expire_date', 'further'),
        )
    )
