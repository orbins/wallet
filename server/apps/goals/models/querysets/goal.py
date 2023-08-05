from django.db.models import QuerySet


class GoalQuerySet(QuerySet):

    def count_uncompleted_goals(self):
        return self.filter(is_completed=False).count()
