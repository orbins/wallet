from django.db.models import Manager

from ..querysets import GoalQuerySet


class GoalManager(Manager):
    def get_queryset(self, **kwargs) -> GoalQuerySet:
        return GoalQuerySet(
            self.model,
            using=self._db,
        )

    def count_uncompleted_goals(self):
        return self.get_queryset().count_uncompleted_goals()
