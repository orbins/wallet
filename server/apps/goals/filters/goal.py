from django_filters import rest_framework as filters


class GoalFilter(filters.FilterSet):
    # DateFilter
    order_by = filters.OrderingFilter(
        fields=(
            ('-percent', 'higher_percent'),
            ('percent', 'lower_percent'),
            ('-target_amount', 'most_expensive'),
            ('target_amount', 'cheapest'),
            ('date', 'newest'),
            ('-date', 'oldest'),
            ('completion', 'closest'),
            ('-completion', 'further'),
        )
    )
