from django.db.models import Manager

from ..querysets import TransactionCategoryQuerySet


class TransactionCategoryManager(Manager):
    def get_queryset(self, **kwargs) -> TransactionCategoryQuerySet:
        return TransactionCategoryQuerySet(self.model, using=self._db)

    def annotate_with_transaction_sums(self) -> TransactionCategoryQuerySet:
        return self.get_queryset().annotate_with_transaction_sums()

    def annotate_with_goals_counter(self) -> TransactionCategoryQuerySet:
        return self.get_queryset().annotate_with_goals_counter()

    def get_top_with_others(self) -> TransactionCategoryQuerySet:
        return self.get_queryset().get_top_with_others()
