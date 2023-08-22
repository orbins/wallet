from django.db.models import Manager

from ..querysets import GoalQuerySet


class GoalManager(Manager):
    def get_queryset(self, **kwargs) -> GoalQuerySet:
        return GoalQuerySet(
            self.model,
            using=self._db,
        )

    def annotate_with_days_to_goal(self):
        return self.get_queryset().annotate_with_days_to_goal()

    def annotate_with_accumulated_amount(self):
        return self.get_queryset().annotate_with_accumulated_amount()

    def get_analytical_data(self):
        return self.get_queryset().get_analytical_data()
