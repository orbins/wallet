from django.db.models import QuerySet


class GoalQuerySet(QuerySet):

    def count_uncompleted_goals(self):
        return self.filter(is_completed=False).count()

    def get_analyzed_data(self):


    # closest_goals = [goal.days_to_goal for goal in queryset.filter(is_completed=False) if goal.days_to_goal > 0]
    # if len(closest_goals) > 0:
    #     closest_goals.sort()
    #     most_closest_goal = closest_goals[GoalConstants.CLOSEST_GOAL_INDEX]
    # else:
    #     most_closest_goal = None
    #
    # categories = TransactionCategory.objects.filter(
    #     goals__in=queryset.filter(is_completed=True)
    # ).annotate_with_goals_counter().order_by('goals_counter')
    # if len(categories) > 0:
    #     most_successful_category = categories[1].name
    # else:
    #     most_successful_category = None
    # # INDEX
    #
    # categories = TransactionCategory.objects.filter(
    #     goals__in=queryset).annotate_with_goals_counter().order_by(
    #     'goals_counter')
    # if len(categories) > 0:
    #     most_popular_category = categories[1].name
    # else:
    #     most_popular_category = None
    # # INDEX
    #
    # response = {
    #     'uncompleted_goals': queryset.count_uncompleted_goals(),
    #
    #     'total_invested_amount': Deposit.objects.filter(
    #         goal__in=queryset.filter(is_completed=False)
    #     ).aggregate_amount()['total_amount'],
    #
    #     'total_percent_amount': Deposit.objects.filter(
    #         goal__in=queryset,
    #         refill_type=RefillTypes.FROM_PERCENTS
    #     ).aggregate_amount()['total_amount'],
    #
    #     'percent__amount_this_month': Deposit.objects.filter(
    #         refill_type=RefillTypes.FROM_PERCENTS,
    #         created_at__month=timezone.now().month
    #     ).aggregate_amount()['total_amount'],
    #
    #     'most_closest_goal': most_closest_goal,
    #     'most_successful_category': most_successful_category,
    #     'most_popular_category': most_popular_category,