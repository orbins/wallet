from django_filters import rest_framework as filters


class GoalFilter(filters.FilterSet):

    order_by = filters.OrderingFilter(
        fields=(
            ('percent', 'percent'),
            ('target_amount', 'amount'),
            ('created_at', 'date'),
            ('expire_date', 'expire_date')
        )
    )
